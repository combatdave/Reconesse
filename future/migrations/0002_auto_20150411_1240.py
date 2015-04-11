# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('future', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
    ]
