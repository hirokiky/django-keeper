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
class Root:
    def __acl__(self):
        return [
            (Allow, Authenticated, 'view_dashboard'),
            (Allow, Authenticated, 'add_issue'),
        ]
```

```python
KEEPER_GLOBAL_CONTEXT = 'path.to.Root'
```

Applying `keeper` for views.

```python
from keeper import keeper


# Global Permissions
@keeper('add_issue')
def issue_list(request):
    """ View requires 'add_issue' permission of Root Context
    """


# Model Permissions
@keeper('view', Issue, lambda request, issue_id: {'id': issue_id})
def issue_detail(request, issue_id):
    """ View requires 'view' permission of Issue model

    * An issue object will be retrieved
    * keeper will check whether the rquests has 'view' permission for the issue

    The third argument function can return keyword argument to retrieve the issue object.
    """
    request.k_context  # Will be instance of the issue object
    ...



@keeper('add_comment', Issue, lambda request, issue_id: {'id': issue_id})
def add_comment(request, issue_id):
    ...

```

## Principals

These `Authenticated`, `Everyone` or so is called `principals`.
Principals is objects that will be used for permissions checking.
In other words, principals are authenticated information.

Default principals in `keeper.security.root_principals`.

* `keeper.security.Everyone`: For all of users
* `keeper.security.Authenticated`: For authenticated users
* `user`: Authenticated user object itself
* `keeper.security.Staff`: For `is_staff` users

### Own principals

You can also add your additional principals.

principals is dict that will store some principal objects.
principal objects can be any type of objects.

principals is authenticated information that can be extracted from request.

```python
def myapp_principals(request):
    principals = {}

    if request.user.is_authenticated:
        principals["team"] = request.user.team

    return principals

```

And you should specify the place of function.

```python
KEEPER_PRINCIPALS_CALLBACKS = [
    'keeper.security.root_principals',
    'myapp.security.myapp_principals',
]
```

Then you can use added prencipals in `__acl__`.
In this case `Project` can be edited by users who belongs to `team`.

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
