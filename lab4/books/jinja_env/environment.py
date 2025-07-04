from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

def url_for(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': url_for,
    })
    return env
