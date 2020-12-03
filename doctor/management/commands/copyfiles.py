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
    origen = '/var/www/claro_usa/'

    def handle(self, *args,**options):
	
	#m = Mediasection.objects.all()
	#for x in m:
	    #comando = 'cp %s%s /var/www/copiaclaro/%s'%(self.origen,x.webimage,x.webimage)
	    #print comando
	    #print os.system("%s"%(comando))

	'''
	banco = [] #Bancoimg.objects.all()
	for x in banco:
	    comando = 'cp %s%s /var/www/copiaclaro/%s'%(self.origen,x.original,x.original)
	    print comando
	    print os.system("%s"%(comando))


	    comando = 'cp %s%s /var/www/copiaclaro/%s'%(self.origen,x.webimage,x.webimage)

	    print comando
	    print os.system("%s"%(comando))




	    comando = 'cp %s%s /var/www/copiaclaro/%s'%(self.origen,x.recorte,x.recorte)

	    print comando
	    print os.system("%s"%(comando))

	b = Bancodwfile.objects.all()
	for x in b:
            comando = 'cp %s%s /var/www/copiaclaro/%s'%(self.origen,x.descargar,x.descargar)
            print comando
            print os.system("%s"%(comando))

	b = Downloade.objects.all()
	for x in b:
            comando = 'cp %s%s /var/www/copiaclaro/%s'%(self.origen,x.dfile,x.dfile)
            print comando
            print os.system("%s"%(comando))


	'''
	b = Videofiles.objects.all()
	for x in b:
            comando = 'cp %s%s /var/www/copiaclaro/%s'%(self.origen,x.videof,x.videof)
            print comando
            print os.system("%s"%(comando))



        return None

