from django import template
from django.utils.safestring import mark_safe
from wiki import utils

register = template.Library()


@register.filter(name='markdown')
def markdown(value):
    return mark_safe(utils.markdownify(value))


# Retrieves all live pages. which are children of the calling page
# for standard index listing
@register.inclusion_tag(
    'wiki/tags/section_listing.html',
    takes_context=True
)
def section_listing(context, calling_page):
    pages = calling_page.get_children().live()
    return {
        'pages': pages,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
