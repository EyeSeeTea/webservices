from django.conf.urls import url
from django.conf import settings
from revproxy.views import ProxyView
from ipware.ip import get_ip

class CustomProxyView(ProxyView):
    upstream = settings.TARGET

    def get_request_headers(self):
        headers = super(CustomProxyView, self).get_request_headers()
        new_headers = {'X-Forwarded-For': get_ip(self.request)}
        return dict(headers, **new_headers)

urlpatterns = [
    url(r'^(?P<path>.*)$', CustomProxyView.as_view()),
]