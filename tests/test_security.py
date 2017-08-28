from unittest.mock import Mock

from django.test import TestCase, RequestFactory

from keeper.security import (
    detect_permissions,
    Allow,
)
from keeper.operators import (
    Everyone,
    Authenticated,
)


dummy_user = Mock(
    is_authenticated=True,
    is_staff=False,
)

dummy_staff = Mock(
    is_authenticated=True,
    is_staff=True,
)


rf = RequestFactory()


class Model:
    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'edit'),
        ]


class TestDetectPermissions(TestCase):
    def test_it(self):
        req = rf.get('/')
        req.user = dummy_user
        actual = detect_permissions(Model(), req)
        self.assertEqual(actual, {'view', 'edit'})
