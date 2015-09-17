from django.contrib.auth.models import User

def is_translator(u):
    if u:
        if u.groups.filter(name='translators'):
            return True
    return False