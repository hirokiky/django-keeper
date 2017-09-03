from importlib import import_module

from django.conf import settings


# Actions
Allow = 'allow'
Deny = 'deny'


def import_module_inner(path):
    try:
        module, func = path.rsplit('.', 1)
    except ImportError:
        return None
    return getattr(import_module(module), func, None)


GlobalContext = None


def initialize_global_context():
    if not hasattr(settings, 'KEEPER_GLOBAL_CONTEXT'):
        return

    global GlobalContext
    GlobalContext = import_module_inner(settings.KEEPER_GLOBAL_CONTEXT)


def detect_permissions(context, request):
    if not hasattr(context, '__acl__'):
        raise TypeError("Context %s doesn't have __acl__ attribute" % context)

    permissions = set()
    acl = context.__acl__()
    for action, operator, permission in acl:
        if isinstance(permission, tuple):
            p = set(permission)
        else:
            p = {permission}

        if isinstance(operator, type):
            o = operator()
        else:
            o = operator

        if o(request):
            if action is Allow:
                permissions |= p
            elif action is Deny:
                permissions -= p
    return permissions


def has_permission(permission, context, request):
    permissions = detect_permissions(context, request)
    return permission in permissions


def has_global_permission(permission, request):
    context = GlobalContext()
    return has_permission(permission, context, request)
