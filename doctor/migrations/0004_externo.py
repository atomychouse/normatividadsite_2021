# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_bancoimg_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Externo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('orden', models.IntegerField(default=1)),
                ('publicado', models.BooleanField(default=False)),
                ('archivomain', models.FileField(upload_to='static/externos')),
                ('originalname', models.CharField(max_length=255)),
                ('typofile', models.CharField(max_length=100)),
                ('rowpk', models.ForeignKey(to='doctor.Rowsection')),
            ],
        ),
    ]
