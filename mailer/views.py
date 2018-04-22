"""Views for mailer"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy
from django_filters.views import FilterView

from accounts.models import User
from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from blocks.models import TemplateBlocks
from mailer.models import EmailWrapper, Unsubscribe, Mailing, MailingTemplate
from mailer.forms import UnsubscribeForm, MailingTemplateForm
from mailer.filters import MailingTemplateFilter



class MailingTemplateListView(OrganizationViewMixin, ManageViewMixin,
                              FilterView):
    """List all mailing templates"""
    model = MailingTemplate
    paginate_by = 10
    context_object_name = 'mailing_templates'
    filterset_class = MailingTemplateFilter
    template_name_suffix = '_list'


class MailingTemplateObjectView(object):
    """Mixin that handles views that create or edit mailing templates"""
    def get_form(self):
        """Get the form"""
        form = super(MailingTemplateObjectView, self).get_form()
        form.fields['tags'].queryset = form.fields['tags'].queryset.filter(
            organization=self.request.organization)
        form.fields['blocks'].queryset = form.fields['blocks'].queryset.filter(
            organization=self.request.organization)
        return form

    def form_valid(self, form):
        """Handle a valid form"""
        result = super(MailingTemplateObjectView, self).form_valid(form)

        TemplateBlocks.objects.filter(template=self.object).delete()
        for block in form.cleaned_data['blocks']:
            templateblock = TemplateBlocks()
            templateblock.template = self.object
            templateblock.block = block
            templateblock.save()

        return result


class MailingTemplateCreateView(ManageViewMixin, SuccessMessageMixin,
                                MailingTemplateObjectView,
                                OrganizationCreateViewMixin, CreateView):
    """Create a template"""
    model = MailingTemplate
    form_class = MailingTemplateForm
    success_url = reverse_lazy('manage:mailer:list_templates')
    success_message = "Template %(name)s was created"


class MailingTemplateUpdateView(ManageViewMixin, SuccessMessageMixin,
                                MailingTemplateObjectView, UpdateView):
    """Update a template"""
    model = MailingTemplate
    form_class = MailingTemplateForm
    success_url = reverse_lazy('manage:mailer:list_templates')
    success_message = "Template %(name)s was edited"
    context_object_name = 'mailing_template'
    slug_field = 'uuid'


class WrapperListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all imports"""
    model = EmailWrapper
    template_name = "mailer/list_wrappers.html"
    paginate_by = 10
    context_object_name = 'wrappers'


class WrapperCreateView(ManageViewMixin, SuccessMessageMixin,
                        OrganizationCreateViewMixin, CreateView):
    """Create a wrapper"""
    model = EmailWrapper
    template_name = 'mailer/create_wrapper.html'
    fields = ['name', 'header', 'footer', 'default']
    success_url = reverse_lazy('manage:mailer:list_wrappers')
    success_message = "Wrapper %(name)s was created"


class WrapperUpdateView(ManageViewMixin, SuccessMessageMixin, UpdateView):
    """Create a wrapper"""
    model = EmailWrapper
    template_name = 'mailer/edit_wrapper.html'
    fields = ['name', 'header', 'footer', 'default']
    context_object_name = 'wrapper'
    success_url = reverse_lazy('manage:mailer:list_wrappers')
    success_message = "Wrapper %(name)s was edited"


class UnsubscribeCreateView(OrganizationViewMixin,
                            OrganizationCreateViewMixin, CreateView):
    """List all imports"""
    model = Unsubscribe
    template_name = "mailer/unsubscribe.html"
    form_class = UnsubscribeForm
    success_url = reverse_lazy('unsubscribe:unsubscribe_complete')

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.origin = 'user'

        if form.cleaned_data['mailing_uuid']:
            form.instance.mailing = Mailing.objects.filter(
                uuid=form.cleaned_data['mailing_uuid']).first()

        if form.cleaned_data['user_uuid']:
            form.instance.user = User.objects.filter(
                username=form.cleaned_data['user_uuid']).first()

        response = super(UnsubscribeCreateView, self).form_valid(form)

        User.objects.filter(email__iexact=form.cleaned_data['email']).update(
            unsubscribed=True)

        return response


class UnsubscribeCompleteView(TemplateView):
    """Page to show after unsubscription is successful"""
    template_name = "mailer/unsubscribe_complete.html"
