from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import RedirectView, TemplateView


urlpatterns = patterns('',
    url(r'^apple-touch-icon\.png$', RedirectView.as_view(
        url='%simg/dh5bp/apple-touch-icon.png' % settings.STATIC_URL,
        permanent=False,
    )),
    url(r'^crossdomain\.xml$', TemplateView.as_view(
        template_name='dh5bp/crossdomain.xml')),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='%simg/dh5bp/favicon.ico' % settings.STATIC_URL,
        permanent=False,
    )),
    url(r'^humans\.txt', TemplateView.as_view(
        template_name='dh5bp/humans.txt')),
    url(r'^robots\.txt', TemplateView.as_view(
        template_name='dh5bp/robots.txt')),
)
