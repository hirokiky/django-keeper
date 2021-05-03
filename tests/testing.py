from unittest.mock import Mock


dummy_user = Mock(
    is_authenticated=True,
    is_staff=False,
)

dummy_staff = Mock(
    is_authenticated=True,
    is_staff=True,
)


class Model:
    def __init__(self, acl_function):
        self.acl_function = acl_function

    def __acl__(self):
        return self.acl_function()
