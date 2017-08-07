from keeper.views import keeper

from core.models import Magazine, Article


@keeper('manage_member', factory=lambda request: request.user.team)
def admin_member(request):
    pass


@keeper('edit', factory=lambda request: request.user.team)
def manage_team(request):
    pass


@keeper('subscribe')
def subscribe_plan(request):
    pass


@keeper('extend', factory=lambda r: r.user.team.subscription)
def extend_subscription(request):
    pass


@keeper('resign', factory=lambda r: r.user.team.subscription)
def resign_subscription(request):
    pass


@keeper('list_magazines')
def magazine_list(request):
    pass


@keeper('read', Magazine, lambda r, mid: {'id': mid})
def magazine_detail(request, magazine_id):
    pass


@keeper('read', Magazine, lambda r, mid: {'id': mid})
def article_list(request, magazine_id):
    pass


@keeper('read', Article, lambda r, aid: {'id': aid})
def article_detail(request, article_id):
    pass
