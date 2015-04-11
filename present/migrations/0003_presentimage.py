# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('present', '0002_entry_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('imageField', models.ImageField(upload_to=b'images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
