class Operator:
    def __call__(self, request):
        raise NotImplementedError


class Everyone(Operator):
    def __call__(self, request):
        return True


class Authenticated(Operator):
    def __call__(self, request):
        return hasattr(request, 'user') and request.user.is_authenticated


class IsUser(Authenticated):
    def __init__(self, user):
        self.user = user

    def __call__(self, request):
        if not super().__call__(request):
            return False
        return self.user == request.user


class Staff(Authenticated):
    def __call__(self, request):
        if not super().__call__(request):
            return False
        return request.user.is_staff
