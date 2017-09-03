# django-keeper

Authorization library for Django, not depends on models.

* Won't depend on models
* Won't save assignments/permissions into datastores

## Install

```bash
$ pip install django-keeper
```

And add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'keeper',
]
```

## At A Glance

Declarative permission mapping for models.

```python
from django.conf import settings
from keeper.security import Allow
from keeper.operations import Everyone, Authenticated, IsUser


class Issue(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    ...

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'add_comment'),
            (Allow, IsUser(self.author), 'edit'),
        ]

```

Instances of model allow:

* Every requests to view
* Autheticated requests to add comments
* it's author to edit

Then, apply `@keeper` for views.

```python
from keeper import keeper


# Model Permissions
@keeper(
    'view',
    model=Issue,
    mapper=lambda request, issue_id: {'id': issue_id})
def issue_detail(request, issue_id):
    """ View requires 'view' permission of Issue model

    * An issue object will be retrieved
    * keeper will check whether the rquests has 'view' permission for the issue

    The third argument function can return keyword argument to retrieve the issue object.
    """
    request.k_context  # Will be instance of the issue object
    ...



@keeper(
    'add_comment',
    model=Issue,
    mapper=lambda request, issue_id: {'id': issue_id})
def add_comment(request, issue_id):
    ...

```

## Global Permission

Not just for model permissions `django-keeper` can handle global permissions.

First, write class having `__acl__` method in models.py.

```python
class Root:
    def __acl__(self):
        return [
            (Allow, Authenticated, 'view_dashboard'),
            (Allow, Authenticated, 'add_issue'),
        ]
```

It's not necessary to put it in `models.py`,
but easy to understand.

And specify it.

```python
KEEPER_GLOBAL_CONTEXT = myapp.models.Root'
```

Then you can use global permission in views.
Simply just apply `@keeper` and permission names.

```python
@keeper('add_issue')
def issue_list(request):
    """ View requires 'add_issue' permission of Root Context
    """

```

## Own Operators

Operators is just `Callable[[HttpRequest], bool]`.
So you can create your own operators easily.

```python
from keeper.operators import Operator, Authenticated


class IsIP(Operator):
    def __init__(self, ip):
        self.ip = ip
        
    def __call__(self, request):
        return request.META.get('REMOTE_ADDR') == self.ip


class BelongsTeam(Authenticated):
    def __init__(self, team, role):
        self.team = team

    def __call__(self, request):
        if not super().__call__(request):
            return False
        return  request.user.team == self.team
```

Use it in ACL

```python
class Article(models.Model):
    team = models.ForeignKey(Team)
    
    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, BelongsTeam(self.team), 'edit'),
            (Allow, IsIP(settings.COMPANY_IP_ADDRESS), 'edit'),
        ]
```

## Alternative

* [django-guardian](https://github.com/django-guardian/django-guardian)
    * It depends on databases
    * Not way to handle global permissions, not just for a model
* [django-rules](https://github.com/dfunckt/django-rules)

## FAQ

* Can I filter models by using ACL?
    * Not supported
