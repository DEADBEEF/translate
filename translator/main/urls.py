from django.conf.urls import patterns, include, url

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
    url(r'^image/(?P<image>[\w\-]+)/$', 'main.views.get_image'),
    # Examples:
    #AJAX
    url(r'^project/start/$', 'main.views.start_project'),
    url(r'^update/page/$', 'main.views.update_page_translation'),
    url(r'^update/notes/$', 'main.views.update_notes'),
    url(r'^get/notes/$', 'main.views.get_note'),
)
