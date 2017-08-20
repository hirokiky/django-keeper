from django.http import Http404
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from keeper.views import keeper, login_required

from core.models import Magazine, Article, Subscription


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
    team = request.k_context
    return TemplateResponse(request, 'core/team_dashboard.html',
                            {'team': team})


@keeper('manage', factory=my_team_factory)
def team_manage(request):
    team = request.k_context
    return TemplateResponse(request, 'core/team_manage.html',
                            {'team': team})


@keeper('manage', factory=my_team_factory)
def team_billing(request):
    team = request.k_context
    subscription = Subscription.objects.filter(team=team).first()
    return TemplateResponse(request, 'core/team_billing.html',
                            {'subscription': subscription,
                             'team': team})


@keeper('managef', factory=my_subscription_factory)
def team_billing_resign(request):
    subscription = request.k_context
    subscription.delete()
    return redirect('team_dashboard')


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
    magazine = request.k_context
    return TemplateResponse(request, 'core/magazine_detail.html',
                            {'magazine': magazine})


@keeper('read',
        model=Article,
        mapper=lambda request, magazine_id, article_id: {'id': article_id})
def article_detail(request, magazine_id, article_id):
    article = request.k_context
    return TemplateResponse(request, 'core/article_detail.html',
                            {'article': article})
