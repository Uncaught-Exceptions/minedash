from django.shortcuts import redirect

from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel)
from wagtail.wagtailforms.models import AbstractFormField
from wagtail.wagtailsearch import index

from wagtailcaptcha.models import WagtailCaptchaEmailForm

from modelcluster.fields import ParentalKey

from wagtailmenus.models import MenuPage

from core.fields import (LinkFields, RelatedLink)


class RedirectPage(MenuPage, LinkFields):

    def serve(self, request):
        return redirect(self.link, permanent=False)

    content_panels = [FieldPanel('title')] + LinkFields.panels


class RichTextPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('core.RichTextPage', related_name='related_links')


class RichTextPage(MenuPage):
    content = RichTextField(blank=True)

    search_fields = MenuPage.search_fields + [
        index.SearchField('content'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('content', classname="full"),
        InlinePanel('related_links', label="Related links"),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(WagtailCaptchaEmailForm, MenuPage):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = [
        FormSubmissionsPanel(),
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
