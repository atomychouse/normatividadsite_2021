# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_remove_bancoimg_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bancoimg',
            name='titulo',
            field=models.CharField(default='', max_length=500, null=True, blank=True),
        ),
    ]
