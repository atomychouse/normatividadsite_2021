# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campainsapp', '0005_auto_20190225_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaincat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('namecat', models.CharField(max_length=200)),
                ('catslug', models.CharField(max_length=255)),
                ('orden', models.IntegerField()),
                ('parentcat', models.ForeignKey(to='campainsapp.Campaincat')),
            ],
        ),
        migrations.CreateModel(
            name='Campcat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campanya', models.ForeignKey(to='campainsapp.Campanya')),
                ('categoria', models.ForeignKey(to='campainsapp.Campaincat')),
            ],
        ),
    ]
