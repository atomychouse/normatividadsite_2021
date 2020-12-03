# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bancodwfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descargar', models.FileField(null=True, upload_to='static/descargas/', blank=True)),
                ('extencion', models.CharField(default='jpg', max_length=20)),
                ('tipo', models.CharField(default='img', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Bancoimg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cats', models.TextField(null=True, blank=True)),
                ('texto', models.TextField(null=True, blank=True)),
                ('titulo', models.CharField(default='', max_length=500, null=True, blank=True)),
                ('original', models.ImageField(null=True, upload_to='static/banco/', blank=True)),
                ('webimage', models.ImageField(null=True, upload_to='static/banco/', blank=True)),
                ('recorte', models.ImageField(null=True, upload_to='static/banco/', blank=True)),
                ('isvideo', models.BooleanField(default=False)),
                ('orden', models.IntegerField(default=0)),
                ('publicado', models.BooleanField(default=False)),
                ('recortar', models.BooleanField(default=False)),
                ('linkvideo', models.CharField(default='', max_length=500, null=True, blank=True)),
            ],
            options={
                'ordering': ['cats'],
            },
        ),
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('catname', models.CharField(max_length=300)),
                ('catslug', models.SlugField(max_length=500)),
                ('parentcat', models.ForeignKey(blank=True, to='doctor.Cat', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Downloade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dtitle', models.CharField(max_length=200, verbose_name='T\xedtulo')),
                ('dfile', models.FileField(upload_to='static/downloadables')),
                ('boxpk', models.IntegerField()),
                ('sending', models.BooleanField(default=False)),
                ('type_link', models.CharField(default='link', max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Downloadmod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dwfile', models.FileField(upload_to='static/downlobles/')),
            ],
        ),
        migrations.CreateModel(
            name='LinkDwn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dtitle', models.CharField(max_length=200, verbose_name='T\xedtulo descarga')),
                ('dfile', models.CharField(max_length=200, verbose_name='Archvo descarga')),
                ('modulo', models.CharField(max_length=200)),
                ('boxpk', models.IntegerField()),
                ('sending', models.BooleanField(default=False)),
                ('type_link', models.CharField(default='link', max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Linkmod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(null=True, upload_to='static/links/', blank=True)),
                ('link', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('publicado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('down_title', models.CharField(max_length=200, verbose_name='T\xedtulo descarga')),
                ('down_file', models.CharField(max_length=200, verbose_name='Archvo descarga')),
            ],
        ),
        migrations.CreateModel(
            name='Mediasection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, blank=True)),
                ('associate_file', models.CharField(max_length=500, null=True, blank=True)),
                ('texto', models.TextField(null=True, blank=True)),
                ('webimage', models.ImageField(null=True, upload_to='static/media/', blank=True)),
                ('orden', models.IntegerField(default=0)),
                ('configs', models.TextField(null=True, blank=True)),
                ('publicado', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permisos', models.TextField(null=True, blank=True)),
                ('grupo', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Rowsection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('module', models.CharField(max_length=100)),
                ('configur', models.TextField(null=True, blank=True)),
                ('orden', models.IntegerField(default=1)),
                ('blankrow', models.CharField(max_length=20, null=True, blank=True)),
                ('name_module', models.CharField(max_length=200, null=True, blank=True)),
                ('publicado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Seccolmenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('col_name', models.CharField(max_length=200, null=True, blank=True)),
                ('slug_col_name', models.CharField(max_length=500, null=True, blank=True)),
                ('orden', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sec_name', models.CharField(max_length=200, verbose_name='Nombre Secci\xf3n')),
                ('sec_slug', models.SlugField(max_length=255, verbose_name='slug')),
                ('page_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo', choices=[('homepage', 'HomePage'), ('bancoimagen', 'banco de Imagenes'), ('intern', 'Interna'), ('links', 'Links')])),
                ('orden', models.IntegerField(default=1)),
                ('webimage', models.CharField(max_length=500, null=True, blank=True)),
                ('mobileimage', models.CharField(max_length=500, null=True, blank=True)),
                ('ishome', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, to='doctor.Section', null=True)),
                ('sec_colum_menu', models.ForeignKey(blank=True, to='doctor.Seccolmenu', null=True)),
                ('sitio', models.ForeignKey(blank=True, to='sites.Site', null=True)),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Textmodule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField(default='')),
                ('publicado', models.BooleanField(default=False)),
                ('rowpk', models.ForeignKey(to='doctor.Rowsection')),
            ],
        ),
        migrations.CreateModel(
            name='Videofiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('videof', models.FileField(upload_to='static/videos')),
                ('converted', models.BooleanField(default=False)),
                ('framimg', models.ImageField(null=True, upload_to='static/videos', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Videomodule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('videoid', models.CharField(max_length=500)),
                ('texto', models.TextField(null=True, blank=True)),
                ('orden', models.IntegerField(default=1)),
                ('imagen', models.ImageField(null=True, upload_to='static/videoimg/', blank=True)),
                ('publicado', models.BooleanField(default=False)),
                ('rowpk', models.ForeignKey(to='doctor.Rowsection')),
            ],
        ),
        migrations.AddField(
            model_name='seccolmenu',
            name='parent',
            field=models.ForeignKey(blank=True, to='doctor.Section', null=True),
        ),
        migrations.AddField(
            model_name='rowsection',
            name='sectionpk',
            field=models.ForeignKey(to='doctor.Section'),
        ),
        migrations.AddField(
            model_name='mediasection',
            name='rowpk',
            field=models.ForeignKey(to='doctor.Rowsection'),
        ),
        migrations.AddField(
            model_name='linkmod',
            name='rowpk',
            field=models.ForeignKey(to='doctor.Rowsection'),
        ),
        migrations.AddField(
            model_name='downloadmod',
            name='secpk',
            field=models.ForeignKey(to='doctor.Section'),
        ),
        migrations.AddField(
            model_name='cat',
            name='secparent',
            field=models.ForeignKey(blank=True, to='doctor.Section', null=True),
        ),
        migrations.AddField(
            model_name='bancoimg',
            name='rowpk',
            field=models.ForeignKey(to='doctor.Rowsection'),
        ),
        migrations.AddField(
            model_name='bancodwfile',
            name='bancopk',
            field=models.ForeignKey(to='doctor.Bancoimg'),
        ),
    ]
