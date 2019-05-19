import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from keeper.operators import Everyone, Authenticated, IsUser, Staff
from.testing import dummy_user, dummy_staff


class TestEveryone:
    def test_it(self, rf):
        req = rf.get('/')
        assert Everyone()(req)


class TestAuthenticated:
    def test_it(self, rf):
        req = rf.get('/')
        req.user = dummy_user
        assert Authenticated()(req)

    def test_no_user(self, rf):
        req = rf.get('/')
        assert not Authenticated()(req)

    def test_not_authenticated(self, rf):
        req = rf.get('/')
        req.user = AnonymousUser()
        assert not Authenticated()(req)


class TestIsUser:
    def test_it(self, rf):
        req = rf.get('/')
        req.user = dummy_user
        assert IsUser(dummy_user)(req)

    def test_not_same_user(self, rf):
        req = rf.get('/')
        req.user = dummy_staff
        assert not IsUser(dummy_user)(req)

    def test_no_user(self, rf):
        req = rf.get('/')
        assert not IsUser(dummy_user)(req)


class TestStaff:
    def test_it(self, rf):
        req = rf.get('/')
        req.user = dummy_staff
        assert Staff()(req)

    def test_no_staff(self, rf):
        req = rf.get('/')
        req.user = dummy_user
        assert not Staff()(req)
