from django.db import models

from keeper.security import Allow
from keeper.operators import Authenticated


class Article(models.Model):
    def __acl__(self):
        return [
            (Allow, Authenticated, 'view'),
        ]
