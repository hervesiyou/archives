from django.conf import settings

def env_variables(request):
    return {
        'HCAPTCHA': settings.APP_HCAPTCHA,
    }