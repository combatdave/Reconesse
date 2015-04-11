# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('present', '0003_presentimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentimage',
            name='imageField',
            field=models.ImageField(upload_to=b'images\\present'),
        ),
    ]
