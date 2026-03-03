import re
from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """Middleware that requires a user to be authenticated to view any page
    except for the ones defined in the ``LOGIN_EXEMPT_URLS`` setting or
    the login url itself.

    Add this class to ``MIDDLEWARE`` *after*
    ``django.contrib.auth.middleware.AuthenticationMiddleware``.

    Example settings:

        LOGIN_URL = 'account:login'
        LOGIN_EXEMPT_URLS = [
            r'^account/register/$',
            r'^account/login/$',  # although login url is always exempted
            r'^admin/',
            r'^media/',
            r'^static/',
        ]
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # compile exempt url patterns
        login_url = settings.LOGIN_URL.lstrip('/')
        self.exempt_urls = [re.compile(login_url)]
        for url in getattr(settings, 'LOGIN_EXEMPT_URLS', []):
            self.exempt_urls.append(re.compile(url))

    def __call__(self, request):
        assert hasattr(request, 'user'), "The authentication middleware must be installed."

        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated:
            # if none of the exempt patterns match, redirect to login
            if not any(m.match(path) for m in self.exempt_urls):
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)
