from django import template

register = template.Library()

@register.filter(name='appartient')
def appartient(liv, user_id):
    return liv.userid_appartient(user_id)

@register.filter(name='appartient_a_famille')
def appartient_a_famille(fam, user_id):
    return fam.appartient(user_id)