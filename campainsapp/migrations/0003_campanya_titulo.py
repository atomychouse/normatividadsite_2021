# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0002_campanya_anyo'),
    ]

    operations = [
        migrations.AddField(
            model_name='campanya',
            name='titulo',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
