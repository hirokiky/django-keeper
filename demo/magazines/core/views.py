from django.http import Http404
from django.template.response import TemplateResponse
from keeper.views import keeper, login_required

from core.models import Magazine, Article


def my_team_factory(request):
    team = request.k_principals.get('team')
    if not team:
        raise Http404
    return team


def my_subscription_factory(request):
    sub = request.k_principals.get('subscription')
    if not sub:
        raise Http404
    return sub


@keeper('view', factory=my_team_factory)
def team_dashboard(request):
    pass


@keeper('manage', factory=my_team_factory)
def team_manage(request):
    pass


@keeper('manage', factory=my_team_factory)
def team_billing(request):
    pass


@keeper('managef', factory=my_subscription_factory)
def team_billing_resign(request):
    pass


@keeper('list_magazines',
        on_fail=login_required())
def dashboard(request):
    plan = request.k_principals.get('plan')
    if plan:
        magazines = request.k_principals['plan'].magazines.all()
    else:
        magazines = Magazine.objects.none()
    return TemplateResponse(request, 'core/dashboard.html',
                            {'magazines': magazines})


@keeper('read',
        model=Magazine,
        mapper=lambda request, magazine_id: {'id': magazine_id})
def magazine_detail(request, magazine_id):
    pass


@keeper('read',
        model=Article,
        mapper=lambda request, magazine_id, article_id: {'id': article_id})
def article_detail(request, magazine_id, article_id):
    pass
