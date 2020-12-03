# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import os
from campainsapp.models import *
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
import StringIO


class Command(BaseCommand):
    help = "convertidor"
    basedir = settings.BASE_DIR



    def resizer(self,imagefile,sizes=800.0):
        
        imagen = Image.open(imagefile.path)
        wi = imagen.width
        hi = imagen.height
        if wi > hi:
            tw = sizes
            th = (tw/wi) * hi
        else:                
            th = sizes
            tw = (th/hi) * wi
        newsize = (int(tw),int(th))
        thumb = imagen.resize(newsize)
        tempcrop = StringIO.StringIO()
        crpedcrop = thumb.save(tempcrop,format=imagen.format)
        cropsafe = ContentFile(tempcrop.getvalue(),imagefile.name)
        return cropsafe



    def videoconverter(self,videopath,cam=None):

        nombrele = videopath.name.split('/')
        ruta = videopath.path
        newrout = ruta.replace(nombrele[-1],'%s_webview.mp4'%(cam.pk))
        try:
            os.remove(newrout)
        except:
            pass
        comand = 'ffmpeg -i %s -vcodec h264 -acodec aac -strict -6 %s'%(videopath.path,newrout)
        comandthumb = 'ffmpeg -i %s -ss 00:00:07.000 -vframes 1 %s/static/campains_crops/%s_tb.jpg'%(videopath.path,settings.BASE_DIR,cam.pk)
        os.system(comand)
        os.system(comandthumb)
        return True



    def handle(self, *args,**options):


        cam = Campanya.objects.filter(statusfile='pendiente')
        for c in cam:
            print c
            if 'image' in c.typofile:
                
                nefc = Campanyafile()
                nefc.campanyapk = c
                nefc.typofile='mini'
                nefc.itemfile = self.resizer(c.original)
                nefc.save()
                

                nefc = Campanyafile()
                nefc.campanyapk = c
                nefc.typofile='desktop'
                nefc.itemfile = self.resizer(c.original,sizes=1024.0)
                nefc.save()



                c.statusfile='converted'
                c.save()



            if 'video' in c.typofile:
                self.videoconverter(c.original,cam=c)
                c.statusfile='converted'
                c.save()
        return None

