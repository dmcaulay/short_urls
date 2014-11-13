# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=255, validators=[django.core.validators.URLValidator(schemes=[b'http', b'https'])])),
                ('code', models.CharField(unique=True, max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
