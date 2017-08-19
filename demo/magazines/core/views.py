from keeper.views import keeper

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


@keeper('list_magazines')
def dashboard(request):
    pass


@keeper('read', Magazine, lambda r, mid: {'id': mid})
def magazine_detail(request, magazine_id):
    pass


@keeper('read', Article, lambda r, aid: {'id': aid})
def article_detail(request, article_id):
    pass
