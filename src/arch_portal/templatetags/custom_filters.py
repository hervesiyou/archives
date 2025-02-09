from django import template

register = template.Library()

@register.filter(name='appartient')
def appartient(liv, user_id):
    return liv.userid_appartient(user_id)