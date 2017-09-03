from django.template import Library
from keeper import security


register = Library()


@register.simple_tag(takes_context=True)
def has_permission(context, obj, permission):
    if obj is None:
        return False

    request = context['request']
    return security.has_permission(permission, obj, request)


@register.simple_tag(takes_context=True)
def has_global_permission(context, permission):
    request = context['request']
    return security.has_global_permission(permission, request)
