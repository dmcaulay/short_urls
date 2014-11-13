import json

from django.shortcuts import render
from django.views.generic import View

from short_urls_app.models import ShortUrl

class ShortUrlRedirectView(View):
    def get(self, request, code):
        short_url = get_object_or_404(ShortUrl, code: code)
        redirect(short_url.url)

class ShortUrlAddView(View):
    def post(self, request):
        url = request.POST.get('url', False)
        if not url:
            return HttpResponseBadRequest("the url is required")
        try:
            short_url = ShortUrl.objects.add(url)
        except: #handle unique key error
            return HttpResponseServerError("unable to shorten %s" % url)
        data = {'short_url': ("http://%s/%s" % request.get_host(), short_url.code)}
        return HttpResponse(json.dumps(data), content_type='application/json')

