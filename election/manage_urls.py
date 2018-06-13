"""URLs for election app"""
from django.conf.urls import url

from election import views


# pylint: disable=invalid-name
urlpatterns = [
    url(r'^$',
        views.OrgElectionListView.as_view(), name='list_elections'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.OrgElectionDetailView.as_view(),
        name='view_election'),
]