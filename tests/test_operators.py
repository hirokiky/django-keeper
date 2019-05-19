import pytest

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from keeper.operators import k_and, k_or, Operator, Everyone, Authenticated, IsUser, Staff
from.testing import dummy_user, dummy_staff
from typing import List

class true(Operator):
    def __call__(self, request):
        return True


class false(Operator):
    def __call__(self, request):
        return False


class TestKAnd:
    def test_true(self, rf):
        actual = k_and(true(), true())
        assert actual(rf.get('/'))

    def test_false(self, rf):
        actual = k_and(true(), false())
        assert not actual(rf.get('/'))

    def test_as_class(self, rf):
        actual = k_and(true, true)
        assert actual(rf.get('/'))

    def test_multiple(self, rf):
        actual = k_and(true, true, true())
        assert actual(rf.get('/'))


class TestKOr:
    def test_true(self, rf):
        actual = k_or(true(), false())
        assert actual(rf.get('/'))

    def test_false(self, rf):
        actual = k_or(false(), false())
        assert not actual(rf.get('/'))

    def test_as_class(self, rf):
        actual = k_or(true, false)
        assert actual(rf.get('/'))

    def test_multiple(self, rf):
        actual = k_or(false, true, true(), false())
        assert actual(rf.get('/'))


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
