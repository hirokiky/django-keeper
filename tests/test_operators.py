from django.contrib.auth.models import AnonymousUser

from keeper.operators import operator, Everyone, Authenticated, IsUser, Staff
from .testing import dummy_user, dummy_staff


@operator
def true(request):
    return True


@operator
def false(request):
    return False


class TestOperatorAnd:
    def test_and_true(self, rf):
        actual = true & true
        assert actual(rf.get('/'))

    def test_and_false(self, rf):
        actual = true & false
        assert not actual(rf.get('/'))

    def test_and_multiple(self, rf):
        actual = true & true & true
        assert actual(rf.get('/'))

    def test_or_true(self, rf):
        actual = true | false
        assert actual(rf.get('/'))

    def test_or_false(self, rf):
        actual = false | false
        assert not actual(rf.get('/'))

    def test_or_multiple(self, rf):
        actual = false | true | true
        assert actual(rf.get('/'))

    def test_xor(self, rf):
        actual = true ^ false
        assert actual(rf.get('/'))

    def test_not(self, rf):
        actual = ~false
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

    def test_user_is_none(self, rf):
        req = rf.get('/')
        req.user = None
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
