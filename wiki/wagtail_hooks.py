from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def editor_js():
    stuff = format_html(
        '<script src="{}"></script>',
        static('wiki/js/simplemde.min.js')
    ) + format_html(
        '<script src="{}"></script>',
        static('wiki/js/simplemde.attach.js')
    )
    return str(stuff)


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('wiki/css/simplemde.min.css')
    )
