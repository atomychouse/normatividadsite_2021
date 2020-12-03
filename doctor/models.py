# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User,Group
import simplejson
from django.contrib.sites.models import Site
import os
from django.db.models import Count
# Create your models here.

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
    #usuario = models.ForeignKey(User)
    grupo = models.ForeignKey(Group)
    permisos = models.TextField(blank=True,null=True)

    def permslist(self):
        try:
            perms = simplejson.loads(self.permisos)
            perms = [int(x) for x in perms]
        except:
            perms = None

        return perms


class Section(models.Model):


    class Meta:
        ordering = ['orden']

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

    def rowssecs(self):
        if self.page_type=='bancoimagen':
            return self.rowsection_set.filter(module='gridbanco')
        else:
            return self.rowsection_set.all()



class Seccolmenu(models.Model):
    parent = models.ForeignKey(Section,blank=True,null=True) 
    #rowpk = models.ForeignKey(Secrowmenu,blank=True,null=True)
    col_name = models.CharField(max_length=200,blank=True,null=True)
    slug_col_name = models.CharField(max_length=500,blank=True,null=True)
    orden = models.IntegerField(default=1);

    class Meta:
        ordering=['orden']

class Rowsection(models.Model):
    sectionpk = models.ForeignKey(Section)
    module = models.CharField(max_length=100)
    configur = models.TextField(blank=True,null=True)
    orden = models.IntegerField(default=1)
    blankrow = models.CharField(max_length=20,blank=True,null=True)
    name_module = models.CharField(max_length=200,blank=True,null=True)
    publicado = models.BooleanField(default=True)

    def configurjson(self):
        return simplejson.dumps(self.configur)

    def modular(self):
        return self.module


    def ligas(self):
        bloques = self.linkmod_set.filter(publicado=True)
        return bloques

    def texts(self):
        bloques = self.textmodule_set.filter(publicado=True)
        return bloques


    def medias(self):
        bloques = self.mediasection_set.filter(publicado=True)
        return bloques


    def vids(self):
        bloques = self.videomodule_set.filter(publicado=True)
        return bloques

    def bancos(self):
        bloques = self.bancoimg_set.filter(publicado=True,isvideo=False).annotate(null_position=Count('cats')).order_by('-null_position','cats')
        return bloques

    def bancovideos(self):
        bloques = self.bancoimg_set.filter(publicado=True,isvideo=True).annotate(null_position=Count('cats')).order_by('-null_position','cats')
        return bloques



    def get_query_set(self):
        if self.page_type=='gridbanco':
            return super(EntryManager, self).get_query_set().filter(module='gridbanco')
        else:
            return super(EntryManager, self).get_query_set().filter()
    
    class Meta:
        ordering = ['orden']


class Textmodule(models.Model):
    rowpk = models.ForeignKey(Rowsection)
    texto  = models.TextField(default='')
    publicado = models.BooleanField(default=False)

    def cleantxt(self):
        if(self.texto):
            response = self.texto.replace('\\n','')
        else:
            response =  ''

        return response

class Linkmod(models.Model):
    rowpk = models.ForeignKey(Rowsection)
    imagen = models.ImageField(upload_to='static/links/',blank=True,null=True)
    link = models.CharField(max_length=255,blank=True,null=True)
    title  = models.CharField(max_length=255,blank=True,null=True)
    publicado = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
            self.imagen.delete()
            super(Linkmod, self).delete(*args, **kwargs)



class Downloadmod(models.Model):
    secpk = models.ForeignKey(Section)
    dwfile = models.FileField(upload_to='static/downlobles/')

    def only_name(self):
        fullname = self.dwfile.name.split('/')
        name = '%s'%fullname[-1:][0]
        return name

    def delete(self, *args, **kwargs):
            self.dwfile.delete()
            super(Downloadmod, self).delete(*args, **kwargs)




class Mediasection(models.Model):
    rowpk = models.ForeignKey(Rowsection)
    title = models.CharField(max_length=200,blank=True,null=True)
    associate_file = models.CharField(max_length=500,blank=True,null=True)
    texto = models.TextField(blank=True,null=True)
    webimage = models.ImageField(upload_to='static/media/',blank=True,null=True)
    orden = models.IntegerField(default=0)
    configs = models.TextField(blank=True,null=True)
    publicado = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
            self.webimage.delete()
            super(Mediasection, self).delete(*args, **kwargs)


    class Meta:
        ordering = ['orden']


    def dictconfigs(self):
        if self.configs:
            return simplejson.loads(self.configs)
        else:
            return None
    
    def downloadsl(self):
        linksdw = []
        linksdw1 = Downloade.objects.filter(boxpk=self.pk).values()
        linksdw2 = LinkDwn.objects.filter(boxpk=self.pk).values()
        linksdw = [linksdw1,linksdw2]

        # EL ORDEN DEL CODIGO ES MUY IMPORTANTE
        lk = [x for x in linksdw2]
        
        for x in lk:
            if x['type_link']=='link':
                x['dfile'] = 'downlobles/%s'%(x['dfile'])
            else:
                pass
        

        for y in linksdw1:
            lk.append(y)



        return lk

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
    publicado = models.BooleanField(default=False)




class Bancoimg(models.Model):
    rowpk = models.ForeignKey(Rowsection)
    cats = models.TextField(blank=True,null=True)
    texto = models.TextField(blank=True,null=True)
    titulo = models.CharField(max_length=500,default='',blank=True,null=True)
    original = models.ImageField(upload_to='static/banco/',blank=True,null=True)
    webimage = models.ImageField(upload_to='static/banco/',blank=True,null=True)
    recorte = models.ImageField(upload_to='static/banco/',blank=True,null=True)
    isvideo = models.BooleanField(default=False)
    orden = models.IntegerField(default=0)
    publicado = models.BooleanField(default=False)
    recortar = models.BooleanField(default=False)
    linkvideo = models.CharField(max_length=500,default='',blank=True,null=True)


    def getvideos(self):
        videos = self.bancodwfile_set.filter(tipo__icontains='video').first()
        if videos:
            link = videos.descargar
        else:
            link = ''
                
        return link


    def mycats(self):
        if self.cats:
            return simplejson.loads(self.cats)
        else:
            return None

    def only_name(self):
        fullname = self.webimage.name.split('/')
        name = '%s'%fullname[-1:][0]
        return name

    def cleantxt(self):
        return self.texto.replace('\\n','<br/>');

    def selfimg(self):
        extx = self.webimage.name.split('.')
        return extx[-1]


    def delete(self, *args, **kwargs):
            self.original.delete()
            self.webimage.delete()
            self.recorte.delete()
            super(Bancoimg, self).delete(*args, **kwargs)



    class Meta:
        ordering=['cats']



class Bancodwfile(models.Model):
    bancopk = models.ForeignKey(Bancoimg)
    descargar = models.FileField(upload_to='static/descargas/',blank=True,null=True)
    extencion = models.CharField(max_length=20,default='jpg')
    tipo = models.CharField(max_length=10,default='img')

    def descarganame(self):
        try:
            name = self.descargar.name.split('.')
            retorno = name[-1]
        except:
            retorno = None


        return retorno

    def delete(self, *args, **kwargs):
            self.descargar.delete()
            super(Bancodwfile, self).delete(*args, **kwargs)




class Cat(models.Model):
    secparent = models.ForeignKey('Section',blank=True,null=True)
    catname = models.CharField(max_length=300)
    catslug = models.SlugField(max_length=500)
    parentcat = models.ForeignKey('Cat',blank=True,null=True)


class LinkDwn(models.Model):
    dtitle = models.CharField(u'Título descarga',max_length=200)
    dfile = models.CharField(u'Archvo descarga',max_length=200)
    modulo = models.CharField(max_length=200)
    boxpk = models.IntegerField()
    sending = models.BooleanField(default=False)
    type_link = models.CharField(max_length=20,blank=True,null=True,default='link')



class Downloade(models.Model):
    dtitle = models.CharField(u'Título',max_length=200)
    dfile = models.FileField(upload_to='static/downloadables')
    #modulo = models.CharField(max_length=200)
    boxpk = models.IntegerField()
    sending = models.BooleanField(default=False)
    type_link = models.CharField(max_length=20,blank=True,null=True,default='link')

    def sends(self):
        if self.sending:
            return self.sending
        else:
            return ''

class Logo(models.Model):
    down_title = models.CharField(u'Título descarga',max_length=200)
    down_file = models.CharField(u'Archvo descarga',max_length=200)


class Videofiles(models.Model):
    videof = models.FileField(upload_to="static/videos")
    converted = models.BooleanField(default=False)
    framimg = models.ImageField(upload_to="static/videos",blank=True,null=True)

    def getimg(self):
        if self.framimg:
            namepices = self.framimg.name.split('/')
            links = '/static/videos/%s'%(namepices[-1])
        else:
            links = None

        return links


    def getvideo(self):
        if self.videof:
            namepices = self.videof.name.split('/')
            links = '/static/videos/%s'%(namepices[-1])
        else:
            links = None

        return links







class Externo(models.Model):
    rowpk = models.ForeignKey(Rowsection)
    title = models.CharField(max_length=100)
    orden = models.IntegerField(default=1)
    publicado = models.BooleanField(default=False)
    archivomain = models.FileField(upload_to='static/externos')
    originalname = models.CharField(max_length=255)
    typofile = models.CharField(max_length=100)