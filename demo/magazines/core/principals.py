def magazines_principals(request):
    principals = set()

    if request.user.is_authenticated:
        team = request.user.team
        principals.add(team)
        principals.add((team, request.user.role))
        principals.add(('role', request.user.role))

        if team.subscription.is_active:
            principals.add(team.subscription.plan)

    return principals
