from django.conf.urls import patterns, url

urlpatterns = patterns(
    'poll',
    url(r'^new/$', 'views.new_poll', name='new'),
    url(r'^list/$', 'views.list_poll', name='list'),
    url(r'^detail/(?P<pk>\d+)/$', 'views.detail_poll', name='detail')
)
