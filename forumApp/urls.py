from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forumApp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "forum.views.main"),
    url(r"^(\d+)/forum/$", "forum.views.forum"),
    url(r"^(\d+)/thread/$", "forum.views.thread"),
    url(r"^post/(new_thread|reply)/(\d+)/$", "forum.views.post"),
    url(r"^new_thread/(\d+)/$", "forum.views.new_thread"),
    url(r"^reply/(\d+)/$", "forum.views.reply"),
    url(r"^profile/(\d+)/$", "forum.views.profile"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),

    url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
      url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
      url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
      url(r'^password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
      url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
      url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),
      #url(r'^accounts/logout/$', RedirectView.as_view(url='')),
      url(r'^accounts/', include('registration.backends.default.urls')),
      #url(r'^accounts/', include('registration.urls')),

)
