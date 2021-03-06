# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 22:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignUpPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('repeat_in_subnav', models.BooleanField(default=False, help_text="If checked, a link to this page will be repeated alongside it's direct children when displaying a sub-navigation for this page.", verbose_name='repeat in sub-navigation')),
                ('repeated_item_text', models.CharField(blank=True, help_text="e.g. 'Section home' or 'Overview'. If left blank, the page title will be used.", max_length=255, verbose_name='repeated item link text')),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('thank_you_text', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('to_address', models.CharField(blank=True, help_text=b'Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name=b'to address')),
                ('from_address', models.CharField(blank=True, max_length=255, verbose_name=b'from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name=b'subject')),
                ('response_message', models.TextField(help_text=b'Message to submittee.')),
                ('response_subject', models.CharField(max_length=255)),
                ('response_from', models.EmailField(max_length=254)),
                ('approved_message', models.TextField(help_text=b'Message to submittee on approval.')),
                ('approved_subject', models.CharField(max_length=255)),
                ('approved_from', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Whitelisted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16)),
                ('uuid', models.UUIDField()),
                ('email', models.EmailField(max_length=254)),
                ('approved', models.BooleanField(default=False)),
                ('approved_on', models.DateTimeField(blank=True, editable=False, null=True)),
                ('submitted_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('signup_page', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='whitelist.SignUpPage')),
            ],
        ),
    ]
