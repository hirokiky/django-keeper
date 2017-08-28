from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from keeper.security import Allow
from keeper.operators import Authenticated, Staff

from .operators import TeamRole, InPlans


ROLE_OWNER = 'OW'
ROLE_MEMBER = 'ME'
ROLE_CHOICES = (
    (ROLE_OWNER, 'Owner'),
    (ROLE_MEMBER, 'Member'),
)


class Root:
    def __acl__(self):
        return [
            (Allow, Authenticated, 'list_magazines'),
        ]


class Team(models.Model):
    name = models.CharField(max_length=20)

    def __acl__(self):
        return [
            (Allow, TeamRole(self, ROLE_OWNER), ('view', 'manage',)),
            (Allow, TeamRole(self, ROLE_MEMBER), ('view',)),
        ]


class User(AbstractUser):
    team = models.ForeignKey(Team, related_name='members',
                             null=True, blank=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

    @property
    def team_subscription(self):
        if not self.team:
            return None
        try:
            subscription = self.team.subscription
        except models.ObjectDoesNotExist:
            return None
        return subscription

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Magazine(models.Model):
    published = models.BooleanField(default=False)

    def __acl__(self):
        if self.published:
            return [
                (Allow, InPlans(self.allowed_plans.all()), 'read')
            ]
        else:
            return [
                (Allow, Staff, 'read'),
            ]


class Article(models.Model):
    magazine = models.ForeignKey(Magazine, related_name='articles')

    def __acl__(self):
        return self.magazine.__acl__()


class Plan(models.Model):
    magazines = models.ManyToManyField(Magazine, related_name='allowed_plans')


class Subscription(models.Model):
    plan = models.ForeignKey(Plan)
    team = models.OneToOneField(Team, related_name='subscription')

    active_until = models.DateTimeField()

    def __acl__(self):
        return [
            (Allow, TeamRole(self.team, ROLE_OWNER), ('manage',)),
        ]

    @property
    def is_active(self):
        return self.active_until <= timezone.now()
