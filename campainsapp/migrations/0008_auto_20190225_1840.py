# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0007_auto_20190225_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaincat',
            name='parentcat',
            field=models.ForeignKey(blank=True, to='campainsapp.Campaincat', null=True),
        ),
    ]
