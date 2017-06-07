import requests
import json

from django import forms
from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from captcha.fields import ReCaptchaField

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, FieldRowPanel)

from wagtail.wagtailforms.models import AbstractForm
from wagtailmenus.models import MenuPage


class Whitelisted(models.Model):
    username = models.CharField(max_length=16)
    uuid = models.CharField(max_length=32)
    email = models.EmailField()
    approved = models.BooleanField(default=False)
    approved_on = models.DateTimeField(
        null=True, blank=True, editable=False)
    submitted_on = models.DateTimeField(
        default=timezone.now, editable=False)
    signup_page = models.ForeignKey(
        'whitelist.SignUpPage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        editable=False
    )

    def clean(self):
        if self.approved:
            try:
                with open(settings.MINECRAFT_WHITELIST_LOCATION) as f:
                    whitelist = json.load(f)
            except IOError as e:
                raise forms.ValidationError(
                    'Unable to open whitelist file: %s' % e)
            except ValueError:
                whitelist = []

            found = False
            for player in whitelist:
                if player['name'] == self.username:
                    raise forms.ValidationError(
                        'Already whitelisted')
            if not found:
                whitelist.append({'name': self.username, 'id': self.uuid})

            with open(settings.MINECRAFT_WHITELIST_LOCATION, "w") as f:
                f.write(json.dumps(whitelist))

            if self.signup_page:
                subject = self.signup_page.approved_subject
                message = self.signup_page.approved_message
                sender = self.signup_page.approved_from
                recipients = [self.email]
                send_mail(subject, message, sender, recipients)

            if not self.approved_on:
                self.approved_on = timezone.now()


class SignUpForm(forms.Form):
    username = forms.RegexField(
        regex=r'^[A-Za-z0-9_]+$',
        label='Your username', max_length=16)
    email = forms.EmailField(label='Your email')
    comment = forms.CharField(
        label='Why we should whitelist you',
        help_text=(
            "Who referred you, or invited you. "
            "Or some other halfway decent reason."),
        max_length=500,
        widget=forms.Textarea)
    captcha = ReCaptchaField(label='')

    def clean_username(self):
        username = self.cleaned_data['username']

        url = "https://api.mojang.com/users/profiles/minecraft/%s" % username

        resp = requests.get(url)
        if resp.status_code != 200:
            raise forms.ValidationError(
                "%s is not an active or valid Minecraft username." % username)
        self.cleaned_data['uuid'] = resp.json()['id']
        return username


class SignUpPage(AbstractForm, MenuPage):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    to_address = models.CharField(
        verbose_name='to address', max_length=255, blank=True,
        help_text=(
            "Optional - form submissions will be emailed to these addresses. "
            "Separate multiple addresses by comma.")
    )
    from_address = models.CharField(
        verbose_name='from address', max_length=255, blank=True)
    subject = models.CharField(
        verbose_name='subject', max_length=255, blank=True)

    response_message = models.TextField(help_text="Message to submittee.")
    response_subject = models.CharField(max_length=255)
    response_from = models.EmailField()

    approved_message = models.TextField(
        help_text="Message to submittee on approval.")
    approved_subject = models.CharField(max_length=255)
    approved_from = models.EmailField()

    def process_form_submission(self, form):
        Whitelisted(
            username=form.cleaned_data['username'],
            uuid=form.cleaned_data['uuid'],
            email=form.cleaned_data['email'],
            signup_page=self).save()

        subject = self.response_subject
        message = self.response_message
        sender = self.response_from
        recipients = [form.cleaned_data['email']]
        send_mail(subject, message, sender, recipients)

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = SignUpForm(request.POST)

            if form.is_valid():
                form.fields.pop('captcha')
                self.process_form_submission(form)

                if self.to_address:
                    addresses = [
                        x.strip() for x in self.to_address.split(',')]
                    content = []
                    for field in form:
                        value = field.value()
                        if isinstance(value, list):
                            value = ', '.join(value)
                        content.append('{}: {}'.format(field.label, value))
                    content = '\n'.join(content)
                    send_mail(
                        self.subject, content, self.from_address, addresses)

                # render the landing_page
                # TODO: It is much better to redirect to it
                return render(
                    request,
                    self.get_landing_page_template(request),
                    self.get_context(request)
                )
        else:
            form = SignUpForm()

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('response_from', classname="col6"),
                FieldPanel('response_subject', classname="col6"),
            ]),
            FieldPanel('response_message'),
        ], "Email response"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('approved_from', classname="col6"),
                FieldPanel('approved_subject', classname="col6"),
            ]),
            FieldPanel('approved_message'),
        ], "approval response"),
    ]
