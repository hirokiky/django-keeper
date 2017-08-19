from importlib import import_module
from functools import lru_cache

from django.conf import settings


# Actions
Allow = 'allow'
Deny = 'deny'

# Principals
Everyone = 'keeper.everyone'
Authenticated = 'keeper.authenticated'
Staff = 'keeper.staff'


def import_module_inner(path):
    module, func = path.rsplit('.', 1)
    return getattr(import_module(module), func)


GlobalContext = None


def initialize_global_context():
    global GlobalContext
    GlobalContext = import_module_inner(settings.KEEPER_GLOBAL_CONTEXT)


@lru_cache(maxsize=1)
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
            funcs.append(import_module_inner(path))
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
