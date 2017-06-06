from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel)


class LinkFields(models.Model):
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    link_external = models.URLField("External link", blank=True)

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        PageChooserPanel('link_page'),
        FieldPanel('link_external'),
    ]

    class Meta:
        abstract = True


# Related links

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True
