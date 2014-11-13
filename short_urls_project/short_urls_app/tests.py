from django.core.exceptions import ValidationError
from django.test import TestCase

from short_urls_app.models import ShortUrl

class ShortUrlTestCase(TestCase):
    def test_creating_a_new_object(self):
        created = ShortUrl.objects.add_short_url('http://www.google.com')
        short_url = ShortUrl.objects.get(url='http://www.google.com')
        self.assertEqual(short_url, created)

    def test_requires_a_valid_url(self):
        with self.assertRaises(ValidationError):
            ShortUrl.objects.add_short_url('invalid')

    def test_it_doesnt_create_duplicates(self):
        ShortUrl.objects.add_short_url('http://www.google.com')
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        ShortUrl.objects.add_short_url('http://www.google.com')
        self.assertEqual(ShortUrl.objects.all().count(), 1)

    def test_raising_unique_code_error(self):
        ShortUrl.objects.create(url='www.someotherurl.com', code='MTchQA')
        with self.assertRaises(ValidationError):
            ShortUrl.objects.add_short_url('http://www.google.com')

class ShortUrlAddViewTestCase(TestCase):
    def test_it_returns_a_short_url(self):
        resp = self.client.post('/', {'url': 'http://www.google.com'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, '{"short_url": "http://testserver/MTchQA"}')
        short_url = ShortUrl.objects.get(url='http://www.google.com')
        self.assertEqual(short_url.url, 'http://www.google.com')
        self.assertEqual(short_url.code, 'MTchQA')

    def test_invalid_url(self):
        resp = self.client.post('/', {'url': 'invalid'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, 'Enter a valid URL.')

    def test_duplicate_error(self):
        ShortUrl.objects.create(url='www.someotherurl.com', code='MTchQA')
        resp = self.client.post('/', {'url': 'http://www.google.com'})
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(resp.content, 'unable to shorten http://www.google.com')

class ShortUrlRedirectViewTestCase(TestCase):
    def test_redirecting_to_the_url(self):
        short_url = ShortUrl.objects.add_short_url('http://www.google.com')
        resp = self.client.get('/{0}'.format(short_url.code))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://www.google.com')

    def test_404s(self):
        resp = self.client.get('/random')
        self.assertEqual(resp.status_code, 404)
