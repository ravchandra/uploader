from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from demo import views as demo_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # Password URL workarounds for Django 1.6: 
    #   http://stackoverflow.com/questions/19985103/
    url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
    url(r'^accounts/password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),
    # ------------------------------------------------------
    url(r'^$', demo_views.home, name='home'),
    url(r'^profile/$', demo_views.profile, name='profile'),
    url(r'^upload_file/$', demo_views.upload_file_view, name='upload_file'),
    url(r'^upload_success/$', demo_views.upload_success_view, name='upload_success'),
]

