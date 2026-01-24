from django.conf import settings

def env_variables(request):
    return {
        'HCAPTCHA': settings.APP_HCAPTCHA,
        "MTN": settings.NO_MTN,
        "ORANGE": settings.NO_ORANGE,
        "SARA": settings.NO_SARA,
        "EMAIL": settings.EMAIL,
        "VERSION": "1.0.1",
    }