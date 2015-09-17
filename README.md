# django-translation-admin
A lightweight translation admin app for Django.

## Installation
This app requires `polib` to be installed. You can do so via pip, with `pip install polib`. More information: http://polib.readthedocs.org/en/latest/

To start using `translationadmin`, simply add the app folder to your project, and then configure a couple of settings as stated below.

In `settings.py`, add `translationadmin` to `INSTALLED_APPS`.

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    ...
    'translationadmin',
    ...
)
```

Also in `settings.py`, add a new list that tells `translationadmin` which apps to include.

```
TRANSLATE_APP_LIST = (
    'planner', # include 'planner' app in the translation admin CP
    'social', # include 'social' app in the translation admin CP
)
```

In your project's `urls.py`, add a new namespace for the app. Make sure the namespace is called `translationadmin`.

```
urlpatterns = patterns('',
    ...
    url(r'^translationadmin/', include('translationadmin.urls', namespace="translationadmin")),
    ...
)
```

You should also already have internationalization enabled in your Django project, and the appropriate settings configured for that. For more: https://docs.djangoproject.com/en/1.8/topics/i18n/translation/

## Troubleshooting
### Common errors
#### Improper permissions
Make sure the user on which your Django project is running has the correct permissions to edit the locale `.mo` and `.po` files. The user will need to have permission to write to those files.
