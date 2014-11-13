import base64
import md5
import re

from django.core.validators import URLValidator
from django.db import models

class ShortUrlManager(models.Manager):
    def add_short_url(self, url):
        short_url = self.filter(url=url)[0]
        if not short_url:
            short_url = self.create(url=url, code=get_code(url))
        return short_url

    # stolen from https://github.com/technoweenie/guillotine/blob/master/lib/guillotine.rb#L37
    # 1. MD5 hash
    # 2. Grab the last 4 bytes
    # 3. Base64 encode
    # 4. Remove trailing junk
    def get_code(url):
        re.sub(r'==\n?$', '', base64.urlsafe_b64encode(md5.new(url).digest()[12:]))

class ShortUrl(models.Model):
    url = models.CharField(max_length=255, unique=True, validators=[URLValidator(schemes=['http','https'])])
    code = models.CharField(max_length=6, unique=True)

    objects = ShortUrlManager()
