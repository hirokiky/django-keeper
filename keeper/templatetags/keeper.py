from django.template import Library
from keeper import security


register = Library()


@register.simple_tag(takes_context=True)
def has_permission(context, obj, permission):
    request = context['request']
    return security.has_permission(permission, obj, request)
