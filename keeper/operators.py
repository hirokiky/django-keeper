class Operator:
    def __call__(self, request):
        raise NotImplementedError

    def __and__(self, other):
        class Combined(Operator):
            def __call__(self_, request):
                return self(request) & other(request)
        return Combined()

    def __or__(self, other):
        class Combined(Operator):
            def __call__(self_, request):
                return self(request) | other(request)
        return Combined()

    def __xor__(self, other):
        class Combined(Operator):
            def __call__(self_, request):
                return self(request) ^ other(request)
        return Combined()

    def __invert__(self):
        class Inverted(Operator):
            def __call__(self_, request):
                return ~self(request)
        return Inverted()


def operator(func):
    class AsOperator(Operator):
        def __call__(self, request):
            return func(request)
    AsOperator.__name__ = func.__name__
    return AsOperator()


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
