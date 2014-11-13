import base64
import md5
import re

from django.core.validators import URLValidator
from django.db import models

class ShortUrlManager(models.Manager):
    def add_short_url(self, url):
        short_url = False
        try:
            short_url = self.get(url=url)
        except ShortUrl.DoesNotExist:
            pass
        if not short_url:
            short_url = ShortUrl(url=url, code=self.get_code(url))
            short_url.full_clean()
            short_url.save()
        return short_url

    # stolen from https://github.com/technoweenie/guillotine/blob/master/lib/guillotine.rb#L37
    # 1. MD5 hash
    # 2. Grab the last 4 bytes
    # 3. Base64 encode
    # 4. Remove trailing junk
    def get_code(self, url):
        return re.sub(r'==\n?$', '', base64.urlsafe_b64encode(md5.new(url).digest()[12:]))

class ShortUrl(models.Model):
    url = models.CharField(max_length=255, unique=True, validators=[URLValidator()])
    code = models.CharField(max_length=6, unique=True)

    objects = ShortUrlManager()
