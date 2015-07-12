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
    url(r'^dresponseToText$', 'chimehack_server.views.dresponseToText', name='dresponseToText'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^verification$', 'chimehack_server.views.verification', name='verification'),
]
