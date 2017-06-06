from django.db.models import TextField

from wagtail.wagtailadmin.edit_handlers import FieldPanel


class MarkdownField(TextField):
    def __init__(self, **kwargs):
        if 'help_text' not in kwargs:
            kwargs['help_text'] = """
            Standard MarkDown should all work, but also see:
            'python markdown' as that is the base library used for rendering,
            and see 'pymdown-extensions' for some other included extensions
            to 'python markdown'.
            """
        super(MarkdownField, self).__init__(**kwargs)

    class Media:
        css = {'all': ('wiki/css/simplemde.min.css', )}
        js = ('wiki/js/simplemde.min.js', 'wiki/js/simplemde.attach.js',)


class MarkdownPanel(FieldPanel):
    def __init__(self, field_name, classname="", widget=None):
        super(MarkdownPanel, self).__init__(field_name, classname, None)

        if self.classname != "":
            self.classname += " "
        self.classname += "markdown"
