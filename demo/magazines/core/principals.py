from django.db.models import ObjectDoesNotExist


def magazines_principals(request):
    principals = {}

    if request.user.is_authenticated and request.user.team:
        team = request.user.team
        principals['team'] = team
        principals['team_role'] = (team, request.user.role)
        principals['role'] = ('role', request.user.role)

        try:
            subscription = team.subscription
        except ObjectDoesNotExist:
            subscription = None

        if subscription and subscription.is_active:
            principals['subscription'] = team.subscription
            principals['plan'] = team.subscription.plan

    return principals
