from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect as django_redirect

from .security import detect_permissions, GlobalContext


def login_required(login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    # FIXME: Ugly hack to extract process when django's user_passes_test.
    return user_passes_test(
        lambda u: False,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )(lambda r: "dummy")


def permission_denied(request, *args, **kwargs):
    return HttpResponseForbidden()


def not_found(request, *args, **kwargs):
    """ Hide page as 404
    * User accessed private contents but not permitted.
    """
    raise Http404


def redirect(name):
    """ Redirect to 'name' page
    * Redirect to "Buy Now" page
    """
    def _redirect(request, *args, **kwargs):
        return django_redirect(name)
    return _redirect


def keeper(permission,
           model=None, mapper=None,
           factory=None,
           on_fail=permission_denied):
    def dec(f):
        @wraps(f)
        def _wrapped(request, *args, **kwargs):
            if mapper:
                model_kwargs = mapper(request, *args, **kwargs)
                context = get_object_or_404(model, **model_kwargs)
            elif factory:
                context = factory(request, *args, **kwargs)
            else:
                context = GlobalContext()

            permissions = detect_permissions(context, request)

            request.k_context = context
            request.k_permissions = permissions

            if permission in permissions:
                return f(request, *args, **kwargs)
            else:
                return on_fail(request, *args, **kwargs)

        return _wrapped
    return dec


class SingleObjectPermissionMixin:
    """ Mixin to check permission for get_object method.
    This Mixin can be used with DetailView, UpdateView, DeleteView and so on.

    ```
    class MyUpdateView(SingleObjectPermissionMixin, UpdateView):
        permission = 'edit'
        on_fail = not_found
        ...
    ```
    """
    permission = None
    on_fail = permission_denied

    class KeeperCBVPermissionDenied(Exception):
        pass

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except self.KeeperCBVPermissionDenied:
            return self.on_fail(request, *args, **kwargs)

    def get_object(self):
        obj = super().get_object()
        permissions = detect_permissions(obj, self.request)

        if self.permission not in permissions:
            raise self.KeeperCBVPermissionDenied

        self.k_permissions = permissions
        return obj


class KeeperDRFPermission:
    """ View peermission class for Django Rest Framework

    ```
    class MyViewset(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewset):
        permission_classes = (KeeperDRFPermission,)
        model_permission = 'manage'
        ...
    ```
    """
    def has_permission(self, request, view):
        perm = getattr(view, 'global_permission', None)
        if perm is None:
            return True

        ctx = GlobalContext()
        permissions = detect_permissions(ctx, request)
        return perm in permissions

    def has_object_permission(self, request, view, obj):
        perm = getattr(view, 'model_permission', None)
        if perm is None:
            return True

        permissions = detect_permissions(obj, request)
        return perm in permissions
