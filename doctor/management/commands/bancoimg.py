# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import os
from doctor.models import *
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = "thumbnail banco Imgs"
    basedir = settings.BASE_DIR


    def handle(self, *args,**options):

        banco = Bancoimg.objects.all()
        for itm in banco:
            pathimg = '%s/%s'%(self.basedir,itm.original)
            if os.path.exists(pathimg):
                imagen = Image.open(pathimg)
                wi = imagen.width
                hi = imagen.height
                if wi > hi:
                    tw = 800.0
                    th = (tw/wi) * hi
                else:                
                    th = 800.0
                    tw = (th/hi) * wi
                newsize = (int(tw),int(th))
                thumb = imagen.resize(newsize)
                name_imagen = '%s/static/banco/recorte.%s'%(settings.BASE_DIR,imagen.format.lower())
                print newsize
                print name_imagen
                thumb.save(itm.webimage.path)
                #print xe
                #itm.recorte = ContentFile(imagen,name_imagen)
                #itm.save()
            else:
                print pathimg,'not exists'

        return None

