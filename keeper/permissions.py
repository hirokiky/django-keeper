from keeper.security import has_permission


class ObjectPermissionBackend(object):
    def authenticate(self, username, password):
        return None

    def has_perm(self, request, perm, obj, *args, **kwargs):
        return has_permission(perm, obj, request)
