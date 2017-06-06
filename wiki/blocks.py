from django import forms
from django.utils.safestring import mark_safe

from wagtail.utils.widgets import WidgetWithScript
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import TextBlock, StreamBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wiki import utils


class MarkdownTextarea(WidgetWithScript, forms.widgets.Textarea):
    def __init__(self, **kwargs):
        super(MarkdownTextarea, self).__init__(**kwargs)

    def render_js_init(self, id_, name, value):
        return 'simplemdeAttach("{0}");'.format(id_)


class MarkdownBlock(TextBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        if 'classname' in kwargs:
            kwargs['classname'] += ' markdown'
        else:
            kwargs['classname'] = 'markdown'
        self.field = forms.CharField(
            required=required, help_text=help_text, widget=MarkdownTextarea())
        super(MarkdownBlock, self).__init__(**kwargs)

    def render_basic(self, value, context):
        return mark_safe(utils.markdownify(value))

    class Media:
        css = {'all': ('wiki/css/simplemde.min.css', )}
        js = (
            'wiki/js/simplemde.min.js',
            'wiki/js/simplemde.attach.js',
        )


class WikiStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
    image = ImageChooserBlock()
    video = EmbedBlock()
