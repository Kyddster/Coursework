from django.contrib.auth import logout

class LogoutOnPageChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and not request.path in ['/magazine/admin', '/magazine/login']:
            logout(request)

        return response