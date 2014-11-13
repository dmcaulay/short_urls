from django.conf.urls import patterns, include, url
from django.contrib import admin

from short_urls_app.views import ShortUrlAddView, ShortUrlRedirectView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', ShortUrlAddView.as_view()),
    url(r'^(?P<code>\w+)', ShortUrlRedirectView.as_view()),
)
