from django.conf import settings
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.message import Message
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

def unread_messages(request):
    count = 0
    if not request.session.get("userid","") : 
        return {'unread_messages_count': count} 
    
    user = request.session['userid']
    if user :
        try: 
            user = get_object_or_404(Membre, pk=user)
            count = Message.objects.filter(destinataire=user, lu=False).count()
        except Membre.DoesNotExist:
            return {'unread_messages_count': count}
    return {'unread_messages_count': count}

def env_variables(request):
    return {
        'HCAPTCHA': settings.APP_HCAPTCHA,
        'URL': settings.URL_SITE,
        "MTN": settings.NO_MTN,
        "ORANGE": settings.NO_ORANGE,
        "SARA": settings.NO_SARA,
        "EMAIL": settings.EMAIL,
        "VERSION": "1.0.1",
    }