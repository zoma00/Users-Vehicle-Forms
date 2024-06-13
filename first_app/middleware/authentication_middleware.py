


from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse  # Import reverse for URL generation


class AuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_url_patterns = [
            '/clients/',  # Protect this specific URL or use regex for broader protection
            # Add other protected patterns as needed
        ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(f"User Authenticated: {request.user.is_authenticated}")  # Print authentication status
        print(f"Accessed URL: {request.path_info}")  # Print accessed URL

        if not request.user.is_authenticated and any(
            pattern in request.path_info for pattern in self.protected_url_patterns
        ):
            return redirect(reverse('login'))  # Redirect to login if not authenticated
        return None










"""
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import path
from first_app import views
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_url_patterns = [  # List of protected URL patterns (regexes)
        path('clients/register', views.register, name='register'),
            # Add more protected patterns as needed
        ]

    def __call__(self, request):
        if not request.user.is_authenticated and any(
            pattern.match(request.path_info) for pattern in self.protected_url_patterns
        ):
            return redirect('/login/')
        response = self.get_response(request)
        return response

"""




"""
class AuthenticationMiddleware(MiddlewareMixin):
    protected_url_patterns = [  # List of protected URL patterns (regexes)
        r'^/clients/',
        # Add more protected patterns as needed
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated and any(
            pattern.match(request.path_info) for pattern in self.protected_url_patterns
        ):
            return redirect('/login/')
        return None
        <list_iterator object at 0x00000194F7F6C190>
pattern 
<URLPattern 'clients/register' [name='register']>
request 
<WSGIRequest: GET '/login'> 
"""