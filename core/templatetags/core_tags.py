from socket import error as socket_error

from django.conf import settings
from django import template

from mcstatus import MinecraftServer

from wagtail.wagtailcore.models import Page

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    return context['request'].site


@register.inclusion_tag('core/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 3:
        # When on the home page or on a root menu item,
        # displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=2)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }


@register.inclusion_tag('core/tags/server_status.html', takes_context=True)
def server_status(context):
    try:
        server = MinecraftServer(settings.MINECRAFT_SERVER_URL)
        status = server.status()

        return {
            'server': settings.MINECRAFT_SERVER_URL,
            'active': True,
            'version': status.version.name,
            'description': status.description['text'],
            'mods': len(status.raw['modinfo']['modList']),
            'request': context['request'],
        }
    except (socket_error, AttributeError):
        return {
            'server': settings.MINECRAFT_SERVER_URL,
            'active': False,
            'request': context['request'],
        }


@register.inclusion_tag('core/tags/who_is_online.html', takes_context=True)
def who_is_online(context):
    try:
        server = MinecraftServer(settings.MINECRAFT_SERVER_URL)
        status = server.status()
        players = status.players.sample

        return {
            'players': {
                'max': status.players.max,
                'online': status.players.online,
                'list': players
            },
            'request': context['request'],
        }
    except (socket_error, AttributeError):
        return {
            'players': None,
            'request': context['request'],
        }
