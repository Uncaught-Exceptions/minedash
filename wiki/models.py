from django.db import models

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, StreamFieldPanel)
from wagtail.wagtailsearch import index


from modelcluster.fields import ParentalKey

from wagtailmenus.models import MenuPage

from core.fields import RelatedLink
from core.models import RedirectPage

from wiki.fields import MarkdownField, MarkdownPanel
from wiki.blocks import WikiStreamBlock


class RedirectWithBlurbPage(RedirectPage):
    blurb = models.TextField(
        max_length=300, help_text="Text visible on section pages.")

    content_panels = RedirectPage.content_panels + [
        FieldPanel('blurb', classname="full"),
    ]
    subpage_types = []


class WikiSectionPage(MenuPage):
    blurb = models.TextField(
        max_length=300, help_text="Text visible on section pages.")
    content = MarkdownField()

    search_fields = MenuPage.search_fields + [
        index.SearchField('content'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('blurb', classname="full"),
        MarkdownPanel('content', classname="full"),
    ]

    subpage_types = [
        'WikiSectionPage', 'BasicWikiPage',
        'WikiPage', 'RedirectWithBlurbPage']


class BasicWikiPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('wiki.BasicWikiPage', related_name='related_links')


class BasicWikiPage(MenuPage):
    blurb = models.TextField(
        max_length=300, help_text="Text visible on section pages.")
    content = MarkdownField()

    search_fields = MenuPage.search_fields + [
        index.SearchField('content'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('blurb', classname="full"),
        MarkdownPanel('content', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]
    subpage_types = []


class WikiPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('wiki.WikiPage', related_name='related_links')


class WikiPage(MenuPage):
    blurb = models.TextField(
        max_length=300, help_text="Text visible on section pages.")
    content = StreamField(WikiStreamBlock())

    search_fields = MenuPage.search_fields + [
        index.SearchField('content'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('blurb', classname="full"),
        StreamFieldPanel('content'),
        InlinePanel('related_links', label="Related links"),
    ]
    subpage_types = []


class MarkdownPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('wiki.MarkdownPage', related_name='related_links')


class MarkdownPage(MenuPage):
    content = StreamField(WikiStreamBlock())

    search_fields = MenuPage.search_fields + [
        index.SearchField('content'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('content'),
        InlinePanel('related_links', label="Related links"),
    ]
