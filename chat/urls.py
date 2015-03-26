from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'chat_room.views.login', name='login'),
    url(r'^chat/', 'chat_room.views.chat_room', name='chat'),
    url(r'^video_chat/', 'chat_room.views.video_chat', name='video_chat'),
    #API
    url(r'^api/v1/consultants/$', 'chat_room.views.all_consultants'),
    url(r'^api/v1/consultants/create$', 'chat_room.views.create_consultant'),
    url(r'^api/v1/consultants/login$', 'chat_room.views.log_in'),
    url(r'^api/v1/consultants/(?P<id>[0-9]+)/available$', 'chat_room.views.set_consultant_available'),
    url(r'^api/v1/consultants/(?P<id>[0-9]+)/busy$', 'chat_room.views.set_consultant_busy'),
    url(r'^api/v1/consultants/(?P<id>[0-9]+)/update_google_id', 'chat_room.views.update_google_id'),
)
