#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

import xadmin
xadmin.autodiscover()
#version 模块自动注册需要版本控制
from xadmin.plugins import  xversion
xversion.register_models()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       #xadmin url
                       # url(r'^$',include(xadmin.site.urls)),
                       url(r'^$', 'markpic.views.home'),
                       url(r'^test/$', 'markpic.views.test'),
                       url(r'^search/$', 'markpic.views.search'),
                       url(r'^login/$', 'markpic.views.login_view'),
                       url(r'^logout/$', 'markpic.views.logout_view'),
                       url(r'^loginprocess$', 'markpic.views.login_view'),
                       url(r'^recommend$', 'markpic.views.recommend'),
                       url(r'^recognition$', 'markpic.views.recogn'),
                       url(r'^analysis$', 'markpic.views.analysis'),
                       url(r'^project$', 'markpic.views.project'),
                       url(r'^account/invalid/$', 'markpic.views.logout_view'),
                       url(r'^user/profile', 'markpic.views.profile'),
                       url(r'^annotation/instruct', 'markpic.views.instruction'),
                       url(r'^corel30k/$', 'markpic.views.processcorel30k'),
                       url(r'^processinit/$', 'markpic.views.processInit'),
                       url(r'^registration/$', 'markpic.views.register'),
                       url(r'^LableMe/$', 'markpic.views.processLableMe'),
                       url(r'^account/loggedin/$', 'markpic.views.loggedin'),
                       url(r'^annotation/process$', 'markpic.views.process'),
                       url(r'^annotation/LableMeAnnotation$', 'markpic.views.LableMeAnnotation'),
                       url(r'^annotation/pagination$', 'markpic.views.paginate'),

                       #extra url
                       url(r'^private$','markpic.views.private'),
                       url(r'^game$','markpic.views.game'),
                       url(r'^api$','markpic.views.game'),

                       #admin replace with xadmin
                       url(r'^admin/',include(xadmin.site.urls),name='xadmin'),
                       #Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.MEDIA_ROOT}, name='media'),
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.STATIC_ROOT}, name='static'),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()

sitemaps = {
    'log5k': 'markpic.views.Log5KSitemap',
}

urlpatterns += (
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)