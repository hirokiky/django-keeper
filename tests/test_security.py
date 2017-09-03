from django.test import TestCase

from keeper.security import (
    detect_permissions,
    Allow,
    Deny,
)
from keeper.operators import (
    Everyone,
    Authenticated,
    IsUser,
)
from .testing import rf, dummy_user, Model


class TestDetectPermissions(TestCase):
    def test_it(self):
        context = Model(lambda: [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'edit'),
        ])
        req = rf.get('/')
        req.user = dummy_user
        actual = detect_permissions(context, req)
        self.assertEqual(actual, {'view', 'edit'})

    def test_no_acl(self):
        req = rf.get('/')
        with self.assertRaises(TypeError):
            detect_permissions(object(), req)

    def test_multiple_permissions(self):
        context = Model(lambda: [
            (Allow, Everyone, ('view', 'edit')),
        ])
        req = rf.get('/')
        actual = detect_permissions(context, req)
        self.assertEqual(actual, {'view', 'edit'})

    def test_operator_object(self):
        context = Model(lambda: [
            (Allow, IsUser(dummy_user), 'view'),
        ])
        req = rf.get('/')
        req.user = dummy_user
        actual = detect_permissions(context, req)
        self.assertEqual(actual, {'view'})

    def test_deny(self):
        context = Model(lambda: [
            (Allow, Everyone, ('view', 'edit')),
            (Deny, IsUser(dummy_user), 'edit'),
        ])
        req = rf.get('/')
        req.user = dummy_user
        actual = detect_permissions(context, req)
        self.assertEqual(actual, {'view'})

        req = rf.get('/')
        actual = detect_permissions(context, req)
        self.assertEqual(actual, {'view', 'edit'})

    def test_not_matched(self):
        context = Model(lambda: [
            (Allow, Authenticated, 'view'),
        ])
        req = rf.get('/')
        actual = detect_permissions(context, req)
        self.assertEqual(actual, set())
