from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from keeper.security import Allow, Authenticated, Staff


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
            (Allow, (self, ROLE_OWNER), ('view', 'manage',)),
            (Allow, (self, ROLE_MEMBER), ('view',)),
        ]


class User(AbstractUser):
    team = models.ForeignKey(Team, related_name='members')
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Magazine(models.Model):
    published = models.BooleanField(default=False)

    def __acl__(self):
        if self.published:
            return [
                (Allow, plan, 'read')
                for plan in self.allowed_plans.all()
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
        # Alternative implementation:
        #     return self.team.__acl__()
        return [
            (Allow, (self.team, ROLE_OWNER), ('manage',)),
        ]

    @property
    def is_active(self):
        return self.active_until <= timezone.now()
