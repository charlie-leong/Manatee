"""
Helper methods that different view use.
"""
from django.conf import settings
from django.shortcuts import redirect

def login_prohibited(view_function):
    """ 
    Decorator function used to prohibit access to a view if the user is not
    logged in.
    """
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function