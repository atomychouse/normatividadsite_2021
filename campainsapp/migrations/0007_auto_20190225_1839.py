# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0006_campaincat_campcat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaincat',
            name='orden',
            field=models.IntegerField(default=1),
        ),
    ]
