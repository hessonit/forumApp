from django.conf.urls import patterns, include, url

from django.contrib import admin
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
    #url(r"^profile/(\d+)/$", "forum.views.profile"),


)
