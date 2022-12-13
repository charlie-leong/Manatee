"""
Helper methods that different view use.
"""
from django.conf import settings
from django.shortcuts import redirect
from .models import Request

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

# Updates the request object with the new form data.
def updateReqEntry(requestObj: Request, formData):
    requestObj.availability = formData.get("availability")
    requestObj.number_of_lessons = formData.get("number_of_lessons")
    requestObj.duration = formData.get("duration")
    requestObj.interval = formData.get("interval")
    requestObj.extra_info = formData.get("extra_info")
    requestObj.save()