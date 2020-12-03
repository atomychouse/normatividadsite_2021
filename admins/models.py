# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import simplejson
from django.contrib.sites.models import Site
# Create your models here.

'''

PAGES_TYPE = (
				('homepage','HomePage'),
				('bancoimagen','banco de Imagenes'),
				('intern','Interna'),
				('links','Links'),
	)


TEMPLATES_DISPOS = (

		('main_carousel','MainCarousel'),
	)


class Permission(models.Model):
	usuario = models.ForeignKey(User)
	permisos = models.TextField(blank=True,null=True)

	def permslist(self):
		try:
			perms = simplejson.loads(self.permisos)
			perms = [int(x) for x in perms]
		except:
			perms = None

		return perms


class Section(models.Model):
	sec_name = models.CharField(u'Nombre Sección',max_length=200)
	sec_slug = models.SlugField(u'slug',max_length=255)
	parent = models.ForeignKey('self',blank=True,null=True)
	page_type = models.CharField(u'Tipo',max_length=50,choices=PAGES_TYPE,blank=True,null=True)
	orden = models.IntegerField(default=1)
	webimage = models.CharField(max_length=500,blank=True,null=True)
	mobileimage = models.CharField(max_length=500,blank=True,null=True)
	ishome = models.BooleanField(default=False)
	sec_colum_menu = models.ForeignKey('Seccolmenu',blank=True,null=True)
	sitio = models.ForeignKey(Site,blank=True,null=True)
	

	def __unicode__(self):
		return self.sec_name
	
	def spheres(self):
		return self.rowsection_set.filter(module='spherenav')


class Secrowmenu(models.Model):
	secpk = models.ForeignKey(Section)
	orden = models.IntegerField(default=1)

class Seccolmenu(models.Model):
	rowpk = models.ForeignKey(Secrowmenu)
	col_name = models.CharField(max_length=200,blank=True,null=True)
	slug_col_name = models.CharField(max_length=500,blank=True,null=True)
	orden = models.IntegerField(default=1);


class Rowsection(models.Model):
	sectionpk = models.ForeignKey(Section)
	module = models.CharField(max_length=100)
	configur = models.TextField(blank=True,null=True)
	orden = models.IntegerField(default=1)
	blankrow = models.CharField(max_length=20,blank=True,null=True)
	name_module = models.CharField(max_length=20,blank=True,null=True)

	def configurjson(self):
		return simplejson.dumps(self.configur)

	def modular(self):
		return self.module

	class Meta:
		ordering = ['orden']


class Textmodule(models.Model):
	rowpk = models.ForeignKey(Rowsection)
	texto  = models.TextField()

	def cleantxt(self):
	    if(self.texto):
		return self.texto.replace('\n','--')
            else:
                return ''


class Linkmod(models.Model):
	rowpk = models.ForeignKey(Rowsection)
	imagen = models.ImageField(upload_to='static/links/',blank=True,null=True)
	link = models.CharField(max_length=255)
	title  = models.CharField(max_length=255)



class Downloadmod(models.Model):
	secpk = models.ForeignKey(Section)
	dwfile = models.FileField(upload_to='static/downlobles/')

	def only_name(self):
		fullname = self.dwfile.name.split('/')
		name = '%s'%fullname[-1:][0]
		return name





class Mediasection(models.Model):
	rowpk = models.ForeignKey(Rowsection)
	title = models.CharField(max_length=200,blank=True,null=True)
	associate_file = models.CharField(max_length=500,blank=True,null=True)
	texto = models.TextField(blank=True,null=True)
	webimage = models.ImageField(upload_to='static/media/',blank=True,null=True)
	orden = models.IntegerField(default=0)
	configs = models.TextField(blank=True,null=True)

	class Meta:
		ordering = ['orden']


	def dictconfigs(self):
		if self.configs:
			return simplejson.loads(self.configs)
		else:
			return None
	
	def downloadsl(self):
		linksdw = LinkDwn.objects.filter(boxpk=self.pk).values()
		return linksdw

	def cleantxt(self):
	    if(self.texto):
		return self.texto.replace('\n','\\n')
            else:
                return ''



class Videomodule(models.Model):
	rowpk = models.ForeignKey(Rowsection)
	title = models.CharField(max_length=100)
	videoid = models.CharField(max_length=500)
	texto = models.TextField(blank=True,null=True)
	orden = models.IntegerField(default=1)
	imagen = models.ImageField(upload_to="static/videoimg/",blank=True,null=True)


class Bancoimg(models.Model):
	rowpk = models.ForeignKey(Rowsection)
	cats = models.TextField(blank=True,null=True)
	texto = models.TextField(blank=True,null=True)
	webimage = models.ImageField(upload_to='static/downlobles/',blank=True,null=True)
	smallimage = models.ImageField(upload_to='static/downlobles/',blank=True,null=True)
	orden = models.IntegerField(default=0)

	def mycats(self):
		return simplejson.loads(self.cats)

	def only_name(self):
		fullname = self.webimage.name.split('/')
		name = '%s'%fullname[-1:][0]
		return name

	def cleantxt(self):
		return self.texto.replace('\\n','<br/>');



class Cat(models.Model):
	catname = models.CharField(max_length=300)
	catslug = models.SlugField(max_length=500)
	parentcat = models.ForeignKey('Cat',blank=True,null=True)


class LinkDwn(models.Model):
	down_title = models.CharField(u'Título descarga',max_length=200)
	down_file = models.CharField(u'Archvo descarga',max_length=200)
	modulo = models.CharField(max_length=200)
	boxpk = models.IntegerField()
	sending = models.BooleanField(default=False)
	type_link = models.CharField(max_length=20,blank=True,null=True,default='link')


'''