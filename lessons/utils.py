from .models import Request

# Updates the request object with the new form data.
def updateReqEntry(requestObj: Request, formData):
    requestObj.availability = formData.get("availability")
    requestObj.number_of_lessons = formData.get("number_of_lessons")
    requestObj.duration = formData.get("duration")
    requestObj.interval = formData.get("interval")
    requestObj.extra_info = formData.get("extra_info")
    requestObj.save()