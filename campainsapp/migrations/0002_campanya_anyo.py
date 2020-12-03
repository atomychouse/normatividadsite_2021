# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campanya',
            name='anyo',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
