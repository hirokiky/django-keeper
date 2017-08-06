from functools import wraps

from django.http import HttpResponseForbidden

from .security import has_permission


def authz(factory, permission):
    """
    from keeper.security import Allow, Everyone


    class Post(models.Model):
        @property
        def __acl__(self):
            return [
                Allow, Everyone, 'view',
                Allow, self.author, 'edit',
            ]

    from myapp.models import Post
    from keeper.security import Staff


    def post_factory(request, post_id):
        return get_object_or_404(Post, id=post_id)


    @authz(post_factory, 'view')
    def post_detail(request, post_id):
        return HttpResponse()
    """

    def dec(f):
        @wraps(f)
        def _wrapped(request, *args, **kwargs):
            context = factory(request, *args, **kwargs)
            request.context = context

            if has_permission(permission, context, request):
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        return _wrapped
    return dec
