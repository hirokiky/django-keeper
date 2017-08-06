from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory


from keeper.security import (
    root_principals,
    detect_permissions,
    Allow,
    Everyone,
    Staff,
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


class TestRootPrincipal(TestCase):
    def test_anonymous(self):
        req = rf.get('/')
        u = AnonymousUser()
        req.user = u
        actual = root_principals(req)
        self.assertEqual(actual, {Everyone, u})

    def test_authenticated(self):
        req = rf.get('/')
        req.user = dummy_user
        actual = root_principals(req)
        self.assertEqual(actual, {Everyone, Authenticated, dummy_user})

    def test_staff(self):
        req = rf.get('/')
        req.user = dummy_staff
        actual = root_principals(req)
        self.assertEqual(actual, {Everyone, Authenticated, Staff, dummy_staff})


class Model:
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit'),
    ]


class TestDetectPermissions(TestCase):
    def test_it(self):
        actual = detect_permissions(Model(), {Everyone, Authenticated})
        self.assertEqual(actual, {'view', 'edit'})
