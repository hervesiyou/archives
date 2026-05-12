from django import template

register = template.Library()

EXCHANGE_RATE = {
    "XAF":1,
    "DC":5
}

@register.filter(name="convertXAFDC")
def convertXAFToDC(somme:float):
    return round((somme / EXCHANGE_RATE.get("DC")))

@register.filter(name="convertDCXAF")
def convertDCToXAF(somme:float):
    return round((somme * EXCHANGE_RATE.get("DC")))

@register.filter(name='appartient')
def appartient(liv, user_id):
    return liv.userid_appartient(user_id)

@register.filter(name='appartient_a_famille')
def appartient_a_famille(fam, user_id):
    return fam.appartient(user_id)

@register.filter(name='make_initials')
def make_initials(username):
    """
    Transforme un nom complet en initiales
    Ex: "Jean Pierre Nguetchueng" → "JPN"
    """
    if not username:
        return "??"
    
    words = username.strip().split()
    if len(words) == 0:
        return "??"
    elif len(words) == 1:
        return words[0][:2].upper() 
    else:
        # Prend la première lettre de chaque mot (max 3)
        initials = ''.join(word[0] for word in words[:3])
        return initials.upper()