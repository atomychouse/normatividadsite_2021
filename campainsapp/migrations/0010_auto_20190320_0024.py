# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0009_campanya_statuscamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campanya',
            old_name='statuscamp',
            new_name='statuscampa',
        ),
    ]
