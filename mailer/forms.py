"""Forms for mailer app"""
from django import forms

from mailer.models import Unsubscribe, Email, MailingTemplate


class UnsubscribeForm(forms.ModelForm):
    """Unsubscribe form"""
    mailing_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)
    user_uuid = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta(object):
        """Meta options for form"""
        model = Unsubscribe
        fields = ['email', 'mailing_uuid', 'user_uuid']


class MailingTemplateForm(forms.ModelForm):
    """Main template form"""
    class Meta(object):
        """Meta options for form"""
        model = MailingTemplate
        fields = ['name', 'deadline_type', 'days_to_deadline', 'election_type']


class EmailForm(forms.ModelForm):
    """Email form"""

    class Meta(object):
        """Meta options for form"""
        model = Email
        fields = ['from_name', 'subject', 'pre_header', 'body_above',
                  'body_below', 'blocks']
