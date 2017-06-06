from markdown import markdown

from markdown import Extension
from markdown.extensions.tables import TableProcessor
from markdown.util import etree


class CustomeTableProcessor(TableProcessor):
    """ Process Tables. """

    def run(self, parent, blocks):
        """ Parse a table block and build table. """
        block = blocks.pop(0).split('\n')
        header = block[0].strip()
        rows = [] if len(block) < 3 else block[2:]

        # Get alignment of columns
        align = []
        for c in self.separator:
            c = c.strip()
            if c.startswith(':') and c.endswith(':'):
                align.append('center')
            elif c.startswith(':'):
                align.append('left')
            elif c.endswith(':'):
                align.append('right')
            else:
                align.append(None)

        # Build table
        table = etree.SubElement(parent, 'table')
        table.set('class', 'table table-striped')
        thead = etree.SubElement(table, 'thead')
        self._build_row(header, thead, align)
        tbody = etree.SubElement(table, 'tbody')
        if len(rows) == 0:
            # Handle empty table
            self._build_empty_row(tbody, align)
        else:
            for row in rows:
                self._build_row(row.strip(), tbody, align)


class TableExtension(Extension):
    """ Add tables to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of TableProcessor to BlockParser. """
        if '|' not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append('|')
        md.parser.blockprocessors.add('table',
                                      CustomeTableProcessor(md.parser),
                                      '<hashheader')


def makeExtension(*args, **kwargs):
    return TableExtension(*args, **kwargs)


def markdownify(content):
    return markdown(
        content,
        [
            'pymdownx.extra',
            'pymdownx.tilde',
            TableExtension(),
            'markdown.extensions.admonition',
            'markdown.extensions.codehilite',
            'markdown.extensions.headerid',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.smarty',
            'markdown.extensions.toc',
            'markdown.extensions.wikilinks',
        ],
    )
