from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db import connections


# Backend based off of https://docs.djangoproject.com/en/4.2/topics/auth/customizing/
# Modification to the Django backend to use MySQL instead of Django's Model system
class MyExternalAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password))
            result = cursor.fetchone()

        if result is not None:
            user = User.objects.get_or_create(first_name=result[1], last_name=result[2], email=result[3], password=result[4])[0]
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
