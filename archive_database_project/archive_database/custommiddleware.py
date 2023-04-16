from django.contrib.auth import logout
from django.contrib.auth.models import User

# runs on page change
class LogoutOnPageChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and not request.path in ['/magazine/admin', '/magazine/login', '/magazine/keywords', '/favicon.ico']:
            uid = request.user.id
            logout(request)
            User.objects.filter(id=uid).delete()

        return response