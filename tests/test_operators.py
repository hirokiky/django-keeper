from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from keeper.operators import Everyone, Authenticated, IsUser, Staff
from.testing import rf, dummy_user, dummy_staff


class TestEveryone(TestCase):
    def test_it(self):
        req = rf.get('/')
        self.assertTrue(Everyone()(req))


class TestAuthenticated(TestCase):
    def test_it(self):
        req = rf.get('/')
        req.user = dummy_user
        self.assertTrue(Authenticated()(req))

    def test_no_user(self):
        req = rf.get('/')
        self.assertFalse(Authenticated()(req))

    def test_not_authenticated(self):
        req = rf.get('/')
        req.user = AnonymousUser()
        self.assertFalse(Authenticated()(req))


class TestIsUser(TestCase):
    def test_it(self):
        req = rf.get('/')
        req.user = dummy_user
        self.assertTrue(IsUser(dummy_user)(req))

    def test_not_same_user(self):
        req = rf.get('/')
        req.user = dummy_staff
        self.assertFalse(IsUser(dummy_user)(req))

    def test_no_user(self):
        req = rf.get('/')
        self.assertFalse(IsUser(dummy_user)(req))


class TestStaff(TestCase):
    def test_it(self):
        req = rf.get('/')
        req.user = dummy_staff
        self.assertTrue(Staff()(req))

    def test_no_staff(self):
        req = rf.get('/')
        req.user = dummy_user
        self.assertFalse(Staff()(req))
