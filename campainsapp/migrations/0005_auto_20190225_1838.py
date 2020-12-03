# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0004_campaincat_campcat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaincat',
            name='parentcat',
        ),
        migrations.RemoveField(
            model_name='campcat',
            name='campanya',
        ),
        migrations.RemoveField(
            model_name='campcat',
            name='categoria',
        ),
        migrations.DeleteModel(
            name='Campaincat',
        ),
        migrations.DeleteModel(
            name='Campcat',
        ),
    ]
