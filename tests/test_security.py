import pytest

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
from .testing import dummy_user, Model


class TestDetectPermissions:
    def test_it(self, rf):
        context = Model(lambda: [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'edit'),
        ])
        req = rf.get('/')
        req.user = dummy_user
        actual = detect_permissions(context, req)
        assert actual == {'view', 'edit'}

    def test_no_acl(self, rf):
        req = rf.get('/')
        with pytest.raises(TypeError):
            detect_permissions(object(), req)

    def test_multiple_permissions(self, rf):
        context = Model(lambda: [
            (Allow, Everyone, ('view', 'edit')),
        ])
        req = rf.get('/')
        actual = detect_permissions(context, req)
        assert actual == {'view', 'edit'}

    def test_operator_object(self, rf):
        context = Model(lambda: [
            (Allow, IsUser(dummy_user), 'view'),
        ])
        req = rf.get('/')
        req.user = dummy_user
        actual = detect_permissions(context, req)
        assert actual == {'view'}

    def test_deny(self, rf):
        context = Model(lambda: [
            (Allow, Everyone, ('view', 'edit')),
            (Deny, IsUser(dummy_user), 'edit'),
        ])
        req = rf.get('/')
        req.user = dummy_user
        actual = detect_permissions(context, req)
        assert actual == {'view'}

        req = rf.get('/')
        actual = detect_permissions(context, req)
        assert actual == {'view', 'edit'}

    def test_not_matched(self, rf):
        context = Model(lambda: [
            (Allow, Authenticated, 'view'),
        ])
        req = rf.get('/')
        actual = detect_permissions(context, req)
        assert actual == set()
