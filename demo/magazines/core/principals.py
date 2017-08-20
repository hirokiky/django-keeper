def magazines_principals(request):
    principals = {}

    if request.user.is_authenticated and request.user.team:
        team = request.user.team
        principals['team'] = team
        principals['team_role'] = (team, request.user.role)
        principals['role'] = ('role', request.user.role)

        if team.subscription.is_active:
            principals['plan'] = team.subscription.plan

    return principals
