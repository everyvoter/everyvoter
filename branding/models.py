"""Models related to different organizations"""
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property

from branding.utils import org_domain_cache_key
from everyvoter_common.utils.models import TimestampModel


class Organization(TimestampModel):
    """Organization holding an EveryVoter Account"""
    name = models.CharField('Name', max_length=50)
    homepage = models.URLField('Homepage')
    platform_name = models.CharField('Platform Name', max_length=50)
    primary_domain = models.ForeignKey(
        'Domain', verbose_name='Primary Domain',
        help_text='Domain to attach all links to',
        related_name='primary_domain', null=True, default=None,
        on_delete=models.SET_NULL)
    elections = models.ManyToManyField(
        'election.Election', through='election.OrganizationElection')
    privacy_url = models.URLField('Privacy Policy URL', blank=True)
    terms_url = models.URLField('Terms of Service URL', blank=True)
    main_unsubscribe_url = models.URLField(
        'Main list unsubscribe URL',
        help_text='URL of page where user can submit their email address to '
                  'be unsubscribed from organization\'s main email list',
        blank=True)
    from_address = models.ForeignKey(
        'mailer.SendingAddress', verbose_name='Sending Address',
        related_name='default_organizations',
        on_delete=models.SET_DEFAULT, default=1)
    online_vr = models.BooleanField(
        default=False,
        verbose_name='Use Online Voter Registration Deadline',
        help_text='If offered use the Online Voter Registration deadline as '
                  'the registration deadline for Voter Registration reminders')
    disable_vr_sameday = models.BooleanField(
        default=True,
        verbose_name='Disable Same Day Voter Registration Reminders',
        help_text='In some states, you\'re able to register to vote on the '
                  'same day as you vote (but not necessarily on Election '
                  'Day.) These automatic reminders may overlap with other '
                  'Election Day reminders your organization has scheduled. '
                  'Check this box to disable Voter Registration reminders '
                  'for all states where it\'s possible to register the same '
                  'day you vote (for voting before Election Day)')
    disable_vr_eday = models.BooleanField(
        default=True,
        verbose_name='Disable Election Day Voter Registration Reminders',
        help_text='In some states, you\'re able to register to vote on '
                  'Election Day. These automatic reminders may overlap with '
                  'other Election Day reminders your organization has '
                  'scheduled. Check this box to disable Voter Registration '
                  'reminders for all states where it\'s possible to register '
                  'on Election Day.')
    email_active = models.BooleanField(
        'Bulk email enabled', default=False)

    class Meta(object):
        """Meta options for Organization"""
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __unicode__(self):
        """String representation of the organization"""
        return self.name

    def save(self, *args, **kwargs):
        """Save the organization"""
        for domain in self.domain_set.all():
            cache.delete(org_domain_cache_key(domain.hostname))
        return super(Organization, self).save(*args, **kwargs)

    @cached_property
    def url(self):
        """Formatted URL of the domain"""
        if self.primary_domain:
            host = self.primary_domain.hostname
        else:
            host = Domain.objects.filter(organization=self).first()

        if settings.DEBUG:
            return 'http://{host}'.format(host=host)

        return 'https://{host}'.format(host=host)


class Domain(TimestampModel):
    """Domain that app is hosted at"""
    organization = models.ForeignKey(
        Organization, db_index=True)
    hostname = models.CharField('Hostname', max_length=100, unique=True)

    class Meta(object):
        """Meta options for domain"""
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __unicode__(self):
        """String representation of the domain"""
        return self.hostname


class Theme(models.Model):
    """Theme for website of organization"""
    organization = models.OneToOneField(Organization)

    class Meta(object):
        """Meta options for Theme"""
        verbose_name = "Theme"
        verbose_name_plural = "Themes"
