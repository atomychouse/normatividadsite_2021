# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0011_auto_20190402_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='campanya',
            name='anyo_display',
            field=models.IntegerField(default=2020),
        ),
        migrations.AddField(
            model_name='campanya',
            name='mes_display',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='campanya',
            name='statuscamp',
            field=models.CharField(default='activo', max_length=10),
        ),
    ]
