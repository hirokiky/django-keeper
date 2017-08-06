from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from .security import has_permission, GlobalContext


def keeper(permission,
           model=None, mapper=None,
           factory=None):
    def dec(f):
        @wraps(f)
        def _wrapped(request, *args, **kwargs):
            if model and mapper:
                kwargs = mapper(request, *args, **kwargs)
                context = get_object_or_404(model, **kwargs)
            elif factory:
                context = factory(request, *args, **kwargs)
            else:
                context = GlobalContext()

            request.k_context = context

            if has_permission(permission, context, request):
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        return _wrapped
    return dec
