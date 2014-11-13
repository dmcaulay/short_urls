import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View

from short_urls_app.models import ShortUrl

class ShortUrlRedirectView(View):
    def get(self, request, code):
        short_url = get_object_or_404(ShortUrl, code=code)
        return redirect(short_url.url)

class ShortUrlAddView(View):
    def post(self, request):
        url = request.POST.get('url', False)
        if not url:
            return HttpResponseBadRequest("the url is required")
        try:
            short_url = ShortUrl.objects.add_short_url(url)
        except ValidationError as e:
            err_msg = e.message_dict.get('url', False)
            if err_msg:
                return HttpResponseBadRequest(err_msg)
            return HttpResponseServerError("unable to shorten %s" % url)
        data = {'short_url': "http://{0}/{1}".format(request.get_host(), short_url.code)}
        return HttpResponse(json.dumps(data), content_type='application/json')

