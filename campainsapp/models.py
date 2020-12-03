# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import simplejson
from django.contrib.sites.models import Site




class Pageinfo(models.Model):
	imagen = models.ImageField(upload_to='static/portadas')
	titulo = models.CharField(max_length=200,blank=True,null=True)


class Campanya(models.Model):
	pais= models.CharField(u'Nombre Sección',max_length=200)
	producto = models.CharField(max_length=200)
	pais_slug = models.CharField(max_length=100)
	temporalidad = models.CharField(max_length=200)
	producto_slug = models.CharField(max_length=100)
	temporalidad_slug = models.CharField(max_length=200)
	usuario = models.ForeignKey(User)
	anyo = models.CharField(max_length=10,blank=True,null=True)
	typofile = models.CharField(max_length=200)
	original = models.FileField(upload_to='static/campains_original/')
	statusfile = models.CharField(max_length=50)
	creado = models.DateTimeField(auto_now_add=True)
	titulo=models.CharField(max_length=300,blank=True,null=True)
	destacado = models.BooleanField(default=False)
	statuscamp = models.CharField(max_length=10,default='activo')
        mes_display = models.IntegerField(default=1)
        anyo_display = models.IntegerField(default=2020)
        
	def __unicode__(self):
		return self.pais


	def mini(self):
		try:
			imge = self.campanyafile_set.filter(typofile='mini').first().itemfile.url
		except:
			imge = ''

		return imge


	def fileinfo(self):
		info = '%s Kb'%(self.original.size/1000)
		typofile = self.typofile.upper().replace('/',' | ')
		return '%s %s'%(info,typofile)

	def mycats(self):
		return self.campcat_set.all()



	def myattachs(self):
		mys = self.campanyafile_set.filter(typofile='adjunto')
		mys = [{'pk':x.pk,'files':x.itemfile.url,'name':x.itemfile.name} for x in mys] 
		return mys


	def jsoncats(self):

		lista = [{'pk':x.categoria.pk,'slug':x.categoria.catslug,'namecat':x.categoria.namecat}  for x in self.campcat_set.all()]
		return lista



class Campanyafile(models.Model):
	campanyapk = models.ForeignKey(Campanya)
	typofile = models.CharField(max_length=100)
	itemfile = models.FileField(upload_to='static/campains_crops/')



class Campaincat(models.Model):
	namecat = models.CharField(max_length=200)
	catslug = models.CharField(max_length=255)
	parentcat = models.ForeignKey('Campaincat',blank=True,null=True)
	orden = models.IntegerField(default=1)



class Campcat(models.Model):
	campanya = models.ForeignKey(Campanya)
	categoria = models.ForeignKey(Campaincat)

