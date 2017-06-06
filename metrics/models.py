import datetime

from django.db import models
from django.utils import timezone

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, StreamFieldPanel)
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey

from wagtailmenus.models import MenuPage

from core.fields import RelatedLink
from wiki.blocks import WikiStreamBlock


class MetricSample(models.Model):
    name = models.CharField(max_length=100)
    volume = models.FloatField()
    unit = models.CharField(max_length=100)
    timestamp = models.DateTimeField()


class MetricsPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('metrics.MetricsPage', related_name='related_links')


class MetricsPage(MenuPage):
    content = StreamField(WikiStreamBlock())

    search_fields = MenuPage.search_fields + [
        index.SearchField('content'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('content'),
        InlinePanel('related_links', label="Related links"),
    ]
    subpage_types = []

    @property
    def metrics(self):
        month_timedelta = datetime.timedelta(days=30)
        month_ago = timezone.now() - month_timedelta

        metrics = MetricSample.objects.filter(
            timestamp__gt=month_ago).order_by('timestamp')

        usage_dict = {}

        for sample in metrics:
            sample_dict = {
                'volume': sample.volume, 'unit': sample.unit,
                'timestamp': str(sample.timestamp).split(".")[0]}
            try:
                usage_dict[sample.name]['data'].append(sample_dict)
            except KeyError:
                if sample.unit == "percentage":
                    title = sample.name + " %"
                else:
                    title = sample.name
                usage_dict[sample.name] = {
                    "data": [sample_dict, ],
                    "title": title
                }
        return usage_dict
