# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.template.context import RequestContext
from django.views.generic import View
import datetime
from django.http import HttpResponse
from rudimentario.modelforms import FormCreator
from  doctor.models import *
import simplejson
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib.sites.shortcuts import get_current_site
import os
from django.conf import settings
from django.http import JsonResponse
from campainsapp.models import *
from django.core.management import call_command
from django.core.paginator import Paginator

def checkuser(rq):
    #assert False,rq.user.groups.all()
    if rq.user.groups.filter(name='campains').exists():
        return None
    elif rq.user.username=='santamarca':
        return None
    else:
        return True    

class Index(View):
    template = 'campainsapp/index.html'

    def get(self, request):
        self.template = 'campainsapp/main_templates/configurando.html'

        pax = checkuser(request)
        if pax:
            return redirect('/home/')


        context = {}
        links = []



        year_start = datetime.datetime.now() - datetime.timedelta(days=1095)
        year_end = datetime.datetime.now() + datetime.timedelta(days=1095)


        if request.user.username=='santamarca':

            pendingfiles = Campanya.objects.all().filter(statusfile='pendiente')
            banco = Campanya.objects.all().filter(statusfile='converted',typofile__icontains='image')
            videos = Campanya.objects.all().filter(statusfile='converted',typofile__icontains='video')
        else:
            pendingfiles = request.user.campanya_set.all().filter(statusfile='pendiente')
            banco = request.user.campanya_set.all().filter(statusfile='converted',typofile__icontains='image')
            videos = request.user.campanya_set.all().filter(statusfile='converted',typofile__icontains='video')




        banco = Paginator(banco,2)

        #context['pendingfiles'] = pendingfiles
        #context['banco'] = banco.page(1)
        #context['videos'] = videos
        #context['years'] = xrange(year_start.year,year_end.year)

        response = render(request, self.template, context)
        return response

Index = Index.as_view()


class upsFiles(View):
    template = 'campainsapp/index.html'

    def post(self, request):

        datos = request.POST.copy()


        pais,pais_slug = datos.get('pais'),slugify(datos.get('pais',''))
        producto,producto_slug = datos.get('producto'),slugify(datos.get('producto',''))
        temporalidad,temporalidad_slug = datos.get('temporalidad'),slugify(datos.get('temporalidad',''))
        usuario = request.user
        original = request.FILES['file']
        statusfile = 'pendiente'
        typofile = original.content_type

        data = {
        'pais':pais,
        'pais_slug':pais_slug,
        'producto':producto_slug,
        'producto_slug':producto_slug,
        'temporalidad':temporalidad,
        'temporalidad_slug':temporalidad_slug,
        'usuario':usuario,
        'typofile':typofile,
        'original':original,
        'statusfile':statusfile,
        'anyo':datos.get('anyo',None),
        'titulo':u'%s %s %s'%(pais_slug,producto_slug,temporalidad_slug)

         }


        newcampanya = Campanya(**data)
        newcampanya.save()
        response = JsonResponse([{'ok':'ok','callback':'calldropmain'}],safe=False)


        return response

upsFiles = upsFiles.as_view()


class runComands(View):

    def get(self, request):

        #call_command('converter')
        comand = 'python /%s/manage.py converter'%(settings.BASE_DIR)
        os.system(comand)

        response = JsonResponse([{'ok':'ok'}],safe=False)

        return response

runComands = runComands.as_view()



class getPendings(View):

    def get(self, request):


        if request.user.username=='santamarca':
            reds = Campanya.objects.all().exclude(statusfile='pendiente').order_by('-id')
            pendientes = Campanya.objects.filter(statusfile='pendiente').count()
        else:
            reds = request.user.campanya_set.all().exclude(statusfile='pendiente').order_by('-id')
            pendientes = request.user.campanya_set.filter(statusfile='pendiente').count()

        readys = []


        for r in reds:
        
            if('image' in r.typofile):

                try:
                    itemfile = r.campanyafile_set.all().first().itemfile.url
                    infoitem = r.original.size/1000
                except:
                    itemfile = ''
                    infoitem = 0

                item = {
                    'pk':r.pk,
                    'original':itemfile,
                    'destacado':r.destacado,
                    'info':'%s Kb'%(infoitem),
                    'titulo':r.titulo,
                    'atachs':r.myattachs(),
                    'typefile':r.typofile.upper().replace('/',' | '),
                    'statuscamp':r.statuscamp
                }

            else:

                try: 
                    infoitem = r.original.size/1000
                except:
                    infoitem = 0
                item = {
                    'pk':r.pk,
                    'original':'static/campains_crops/%s_tb.jpg'%(r.pk),
                    'destacado':r.destacado,
                    'video':'/%s'%(r.original.url),
                    'info':'%s Kb'%(infoitem),
                    'titulo':r.titulo,
                    'atachs':r.myattachs(),
                    'typefile':r.typofile.upper().replace('/',' | '),
                    'statuscamp':r.statuscamp
                }


            readys.append(item)


        response = JsonResponse(
            {
            'readys':readys,
            'pends':pendientes,
            'user':request.user.username
            }
            ,safe=False)

        return response

getPendings = getPendings.as_view()





class edtSingle(View):

    def get(self, request):
        data = request.GET.copy()
        if data.get('pk',None):
            campanya = Campanya.objects.get(pk=data.get('pk'))
            hechoes = {
                    'pk':campanya.pk,
                    'pais':campanya.pais,
                    'pais_slug':campanya.pais_slug,
                    'producto':campanya.producto_slug,
                    'producto_slug':campanya.producto_slug,
                    'temporalidad':campanya.temporalidad,
                    'temporalidad_slug':campanya.temporalidad_slug,
                    'usuario':campanya.usuario.pk,
                    'typofile':campanya.typofile,
                    'original':campanya.original.url,
                    'mini':campanya.mini(),
                    'anyo':campanya.anyo,
                    'atachs':campanya.myattachs(),
                    'statuscamp':campanya.statuscamp,
                    'mes_display':campanya.mes_display,
                    'anyo_display':campanya.anyo_display,
                    'titulo':campanya.titulo,
                    'allcats':[{'pk':c.pk,'valu':[sb.pk for sb in c.campaincat_set.all()]} for c in Campaincat.objects.filter(parentcat__isnull=True)],
                    'cats':[x.categoria_id for x in campanya.campcat_set.all()]

            }



        else:
            hechoes=None

        response = JsonResponse(
            {'pens':hechoes
            }
            ,safe=False)

        return response

edtSingle = edtSingle.as_view()




class saveSingle(View):

    def post(self, request):
        data = request.POST.copy()

        if data.get('pk',None):
            campanya = Campanya.objects.get(pk=data.get('pk'))
        else:
            campanya = Campanya()
        


        campanya.campcat_set.all().delete()

        for x in data.getlist('cats[]'):
            c = Campcat(campanya=campanya,categoria_id=x)
            c.save()
	mes = data.get('mes_display',1).split(':')[-1]
	mes = int(mes)
	anyo = data.get('anyo_display',1).split(':')[-1]
	anyo = int(anyo)
        campanya.titulo= data.get('titulo_imagen','')
        campanya.statuscamp=data.get('statuscamp', 'activa')
	campanya.mes_display = mes
	campanya.anyo_display = anyo
	campanya.save()

        response = JsonResponse(
            {'pens':'hechoes'
            }
            ,safe=False)

        return response

saveSingle = saveSingle.as_view()




class delSingle(View):

    def get(self, request):
        data = request.GET.copy()
        if data.get('pk',None):
            campanya = Campanya.objects.get(pk=data.get('pk'))
            os.remove(campanya.original.path)
            
            for c in campanya.campanyafile_set.all():
                os.remove(c.itemfile.path)
                c.delete()
            campanya.delete()
            hechoes = 'done'
        else:
            hechoes=None

        response = JsonResponse(
            {'pens':hechoes
            }
            ,safe=False)

        return response

delSingle = delSingle.as_view()



class editGroup(View):

    def post(self, request):
        data = request.POST.copy()
        context = {}
        dupk = request.POST.getlist('keyg[]')
        camps = Campanya.objects.filter(pk__in=dupk)
        
        year_start = datetime.datetime.now() - datetime.timedelta(days=1095)
        year_end = datetime.datetime.now() + datetime.timedelta(days=1095)
        context['camps'] = camps
        context['years'] = xrange(year_start.year,year_end.year)
        response = render(request,'campainsapp/main_templates/ediciongrupo.html', context)

        return response

editGroup = editGroup.as_view()



class saveGroup(View):

    def post(self, request):
        data = request.POST.copy()
        context = {}
        dupk = request.POST.getlist('keyg[]')
        cats = request.POST.getlist('cats[]')
        camps = Campanya.objects.filter(pk__in=dupk)

        for c in camps:
            c.campcat_set.all().delete()
            for cat in cats: 
                if cat:
                    catcap = Campcat()
                    catcap.campanya_id=c.pk
                    catcap.categoria_id = cat
                    catcap.save()

	    mes = data.get('mes_display',1).split(':')[-1]
	    mes = int(mes)
	    anyo = data.get('anyo_display',1).split(':')[-1]
 	    anyo = int(anyo)
            c.titulo= data.get('titulo_imagen','')
            c.statuscamp=data.get('statuscamp', 'activa')
	    c.mes_display = mes
	    c.anyo_display = anyo
	    c.save()



        response = JsonResponse(
            {'pens':'hechoes'
            }
            ,safe=False)
        return response

saveGroup = saveGroup.as_view()



class rmGroup(View):

    def post(self, request):
        data = request.POST.copy()
        context = {}
        dupk = request.POST.getlist('keyg[]')
        camps = Campanya.objects.filter(pk__in=dupk)

        for x in camps:
            os.remove(x.original.path)
            for i in x.campanyafile_set.all():
                os.remove(i.itemfile.path)
                i.delete()
            x.delete()


        response = JsonResponse(
            {'pens':'hechoes'
            }
            ,safe=False)
        return response

rmGroup = rmGroup.as_view()


class addTocat(View):

    def get(self, request):
        data = request.GET.copy()
        context={}
        pk = data.get('pk',None)
        cpk = data.get('cpk',None)
        act = data.get('action')



        if pk and cpk:
            cc = Campcat.objects.filter(campanya_id=cpk,categoria_id=pk)
            
            if cc.count()>0:
                context['ya']=True
                cc.delete()

            else:
                cc = Campcat()
                cc.campanya_id=cpk
                cc.categoria_id=pk
                cc.save()
                context['added']=True

        response = JsonResponse(context,safe=False)
        return response

addTocat = addTocat.as_view()



class saveAll(View):

    def get(self, request):
        data = request.GET.copy()
        context={}

        miscampanias = request.user.campanya_set.all()
        miscampanias.update(statuscamp='online')
        response = JsonResponse(context,safe=False)
        return response

saveAll = saveAll.as_view()



class allCats(View):

    def get(self, request):
        data = request.GET.copy()
        context={}

        cats = Campaincat.objects.filter(parentcat__isnull=True)
        context['cats']=[
            {
            'pk':x.pk,
            'name':x.namecat,
            'subcats':[{'pk':sx.pk,'name':sx.namecat} for sx in x.campaincat_set.all()]
            } for x in cats 
        ]

        response = JsonResponse(context,safe=False)
        return response

allCats = allCats.as_view()



class Destaca(View):

    def get(self, request):
        data = request.GET.copy()
        context={}

        pk = data.get('pk')

        context['pk']=pk
        c = Campanya.objects.get(pk=pk)
        if data.get('des'):
            c.destacado = True
        else:
            c.destacado = False

        c.save()

        response = JsonResponse(context,safe=False)
        return response

Destaca = Destaca.as_view()




class adjuntaFile(View):
    template = 'campainsapp/index.html'

    def post(self, request):
        original = request.FILES['file']
        datos = request.POST.copy()
        camf = Campanyafile()
        camf.campanyapk_id = datos.get('campk')
        camf.typofile = 'adjunto'
        camf.itemfile = request.FILES['file']
        camsave = camf.save()
        response = JsonResponse([{'ok':'ok'}],safe=False)
        return response
adjuntaFile = adjuntaFile.as_view()
