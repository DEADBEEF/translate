from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    # Login/Account urls
    url(r'^register/$', 'main.views.register'),
    url(r'^login/$', 'main.views.loginView'),
    url(r'^logout/$', 'main.views.logoutView'),
    # Story
    url(r'^story/(?P<book>\w+)/$', 'main.views.notebook'),
    url(r'^story/(?P<book>\w+)/(?P<story>\w+)/$', 'main.views.story'),
    url(r'^story/(?P<book>\w+)/(?P<story>\w+)/(?P<page>\d+)/$', 'main.views.page'),
    # Examples:
    # url(r'^$', 'translator.views.home', name='home'),
    # url(r'^translator/', include('translator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
