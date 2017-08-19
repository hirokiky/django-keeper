from keeper.views import keeper, login_required

from core.models import Magazine, Article


@keeper('view', factory=lambda request: request.user.team)
def team_dashboard(request):
    pass


@keeper('manage', factory=lambda request: request.user.team)
def team_manage(request):
    pass


@keeper('manage', factory=lambda request: request.user.team)
def team_billing(request):
    pass


@keeper('manage', factory=lambda r: r.user.team.subscription)
def team_billing_resign(request):
    pass


@keeper('list_magazines',
        on_fail=login_required())
def dashboard(request):
    pass


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
