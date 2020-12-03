# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0010_auto_20190320_0024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pageinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(upload_to='static/portadas')),
                ('titulo', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='campanya',
            name='statuscampa',
        ),
        migrations.AddField(
            model_name='campanya',
            name='destacado',
            field=models.BooleanField(default=False),
        ),
    ]
