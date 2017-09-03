from keeper.operators import Authenticated


class TeamRole(Authenticated):
    def __init__(self, team, role):
        self.team = team
        self.role = role

    def __call__(self, request):
        if not super().__call__(request):
            return False
        return (
            request.user.team == self.team and
            request.user.role == self.role
        )


class InPlans(Authenticated):
    def __init__(self, plans):
        self.plans = plans

    def __call__(self, request):
        if not super().__call__(request):
            return False
        subscription = request.user.team.subscription
        if not subscription:
            return False
        return self.plans.filter(id=subscription.plan_id).exists()
