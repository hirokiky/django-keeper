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
