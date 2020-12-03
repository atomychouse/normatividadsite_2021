# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0008_auto_20190225_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='campanya',
            name='statuscamp',
            field=models.CharField(default='offline', max_length=10),
        ),
    ]
