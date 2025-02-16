from django.template.defaulttags import register
import environ


@register.filter
def env(key):
    return environ.Env()(key)
