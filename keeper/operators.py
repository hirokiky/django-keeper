def k_and(*operators):
    operators = [o() if isinstance(o, type) else o
                 for o in operators]

    def combined(request):
        return all(o(request) for o in operators)

    return combined


def k_or(*operators):
    operators = [o() if isinstance(o, type) else o
                 for o in operators]

    def combined(request):
        return any(o(request) for o in operators)

    return combined


class Operator:
    def __call__(self, request):
        raise NotImplementedError


class Everyone(Operator):
    def __call__(self, request):
        return True


class Authenticated(Operator):
    def __call__(self, request):
        return hasattr(request, 'user') and request.user.is_authenticated


class IsUser(Operator):
    def __init__(self, user):
        self.user = user

    def __call__(self, request):
        return Authenticated()(request) and self.user == request.user


class Staff(Operator):
    def __call__(self, request):
        return Authenticated()(request) and request.user.is_staff
