from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'chat_room.views.login', name='login'),
    url(r'^chat/', 'chat_room.views.chat_room', name='chat'),
)
