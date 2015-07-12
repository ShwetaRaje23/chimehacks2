from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'chimehack_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'chimehack_server.views.home'),
    url(r'^signup$', 'chimehack_server.views.signup', name='signup'),
    url(r'^settings$', 'chimehack_server.views.settings', name='settings'),
    url(r'^home$', 'chimehack_server.views.home', name='home'),
    url(r'^login$', 'chimehack_server.views.login', name='login'),
]
