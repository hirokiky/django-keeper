from importlib import import_module

from django.conf import settings


# Actions
Allow = 'allow'
Deny = 'deny'

# Principals
Everyone = 'keeper.everyone'
Authenticated = 'keeper.authenticated'
Staff = 'keeper.staff'


class GlobalContext:
    def __acl__(self):
        return settings.KEEPER_GLOBAL_ACL


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


def get_principals_callbacks():
    paths = getattr(settings, 'KEEPER_PRINCIPALS_CALLBACKS', None)
    if paths:
        funcs = []
        for path in paths:
            module, func = path.rsplit('.', 1)
            funcs.append(getattr(import_module(module), func))
        return funcs
    else:
        return [root_principals]


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
    callbacks = get_principals_callbacks()
    principals = set()
    for c in callbacks:
        principals |= c(request)
    permissions = detect_permissions(context, principals)
    return permission in permissions
