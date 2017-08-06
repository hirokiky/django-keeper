from importlib import import_module

from django.conf import settings


# Actions
Allow = 'allow'
Deny = 'deny'

# Principals
Everyone = 'keeper.everyone'
Authenticated = 'keeper.authenticated'
Staff = 'keeper.staff'


def root_principals(request):
    principals = set()
    principals.add(Everyone)
    if hasattr(request, 'user'):
        principals.add(request.user)
        if request.user.is_authenticated:
            principals.add(Authenticated)
        if request.user.is_staff:
            principals.add(Staff)
    return principals


def get_principals_callback():
    path = getattr(settings, 'ACL_AUTHZ_PRINCIPALS_CALLBACK', None)
    if path:
        module, func = path.rsplit('.', 1)
        return getattr(import_module(module), func)
    else:
        return root_principals


def detect_permissions(context, principals):
    if not hasattr(context, '__acl__'):
        raise TypeError("Context %s doesn't have __acl__ attribute" % context)

    permissions = set()
    acl = context.__acl__
    for action, principal, permission in acl:
        if isinstance(permission, tuple):
            p = set(permission)
        else:
            p = {permission}
        if principal in principals:
            if action is Allow:
                permissions |= p
            elif action is Deny:
                permissions -= p
    return permissions


def has_permission(permission, context, request):
    callback = get_principals_callback()
    principals = callback(request)
    permissions = detect_permissions(context, principals)
    return permission in permissions
