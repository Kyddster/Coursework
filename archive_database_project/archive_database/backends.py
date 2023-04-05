from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db import connections

class MyExternalAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password))
            row = cursor.fetchone()

        if row is not None:
            user = User.objects.get_or_create(first_name=row[1], last_name=row[2], email=row[3], password=row[4])[0]
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
