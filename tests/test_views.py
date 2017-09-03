from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from keeper.operators import Authenticated
from keeper.security import Allow
from keeper.views import keeper, login_required

from .models import Article
from .testing import rf, dummy_user


class Root:
    def __acl__(self):
        return [
            (Allow, Authenticated, 'view'),
        ]


class TestKeeper(TestCase):
    def test_global_context(self):
        # TODO
        pass

    def test_model(self):
        def article_detail(request, article_id):
            return "res"

        target = keeper(
            'view',
            model=Article,
            mapper=lambda request, article_id: {
                'id': article_id,
            }
        )(article_detail)

        article = Article.objects.create(id=1)

        req = rf.get('/')
        req.user = dummy_user
        res = target(req, article_id=1)
        self.assertEqual(res, 'res')
        self.assertEqual(req.k_context, article)

    def test_factory(self):
        def my_article(request):
            return "res"

        target = keeper(
            'view',
            factory=lambda request: Article.objects.first()
        )(my_article)

        article = Article.objects.create()

        req = rf.get('/')
        req.user = dummy_user
        res = target(req)
        self.assertEqual(res, 'res')
        self.assertEqual(req.k_context, article)

    def test_on_fail(self):
        def my_article(request):
            return "res"

        target = keeper(
            'view',
            factory=lambda request: Article.objects.first()
        )(my_article)

        Article.objects.create()

        req = rf.get('/')
        res = target(req)
        self.assertEqual(res.status_code, 403)

    def test_on_fail_not_found(self):
        def my_article(request):
            return "res"

        target = keeper(
            'view',
            factory=lambda request: Article.objects.first(),
            on_fail=login_required(login_url='/login/'),
        )(my_article)

        Article.objects.create()

        req = rf.get('/')
        req.user = AnonymousUser()
        res = target(req)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/login/?next=/')
