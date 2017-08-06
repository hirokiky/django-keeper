# django-keeper


Authorization library for Django, not depends on models.

* Won't depend on models
* Won't save assignments/permissions into datastores

## At A Glance

Declarative permission mapping for models.

```python
from django.conf import settings
from keeper import Allow, Everyone, Authenticated


class Issue(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    ...

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'add_comment'),
            (Allow, self.author, 'edit'),
        ]

```

Global permissions.

```python
KEEPER_GLOBAL_ACL = [
    (Allow, Authenticated, view_dashboard'),
    (Allow, Authenticated, add_issue'),
]
```

Applying `keeper` for views.

```python
from keeper import keeper


# Global Permissions
@keeper('add_issue')
def issue_list(request):
    ...


# Model Permissions
@keeper('view', Issue, lambda request, issue_id: {'id': issue_id}):
def issue_detail(request, issue_id):
    request.k_context  # Will be instance of Issue model got by the lambda mapping.
    ...



@keeper('add_comment', Issue, lambda request, issue_id: {'id': issue_id}):
def add_comment(request, issue_id):
    ...

```

### Additional Principals

```python
from keeper.security import root_principals


def myapp_principals(request):
    principals = root_principals(request)

    if request.user.is_authenticated:
        principals.add(request.user.team)

    return principals

```

```python
KEEPER_PRINCIPALS_CALLBACK = 'myapp.security.myapp_principals'
```

Use added prencipal in `__acl__`

```python
class Project(models.Model):
    team = models.ForeginKey('myapp.Team')
    ...

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, self.team, 'edit'),
        ]

```

## Alternative

* [django-guardian](https://github.com/django-guardian/django-guardian)
    * It depends on databases
    * Not way to handle global permissions, not just for a model

## FAQ

* Can I filter models by using ACL?
    * Not supported
