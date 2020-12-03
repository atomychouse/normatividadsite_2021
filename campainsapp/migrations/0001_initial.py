# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campanya',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pais', models.CharField(max_length=200, verbose_name='Nombre Secci\xf3n')),
                ('producto', models.CharField(max_length=200)),
                ('pais_slug', models.CharField(max_length=100)),
                ('temporalidad', models.CharField(max_length=200)),
                ('producto_slug', models.CharField(max_length=100)),
                ('temporalidad_slug', models.CharField(max_length=200)),
                ('typofile', models.CharField(max_length=200)),
                ('original', models.FileField(upload_to='static/campains_original/')),
                ('statusfile', models.CharField(max_length=50)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Campanyafile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typofile', models.CharField(max_length=100)),
                ('itemfile', models.FileField(upload_to='static/campains_crops/')),
                ('campanyapk', models.ForeignKey(to='campainsapp.Campanya')),
            ],
        ),
    ]
