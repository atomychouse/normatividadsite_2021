# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template.context import RequestContext
from django.views.generic import View
import datetime
from django.http import HttpResponse
from rudimentario.modelforms import FormCreator
from  doctor.models import *
import simplejson
from django.template.defaultfilters import slugify
from doctor.models import * 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from base64 import b64decode
from PIL import Image
from io import BytesIO
from django.contrib.sites.shortcuts import get_current_site
import os
from django.contrib.sites.models import Site
from rudimentario.settings import BASE_DIR

class addSec(View):

    context = {}
    
    def get(self,request):
        data = request.GET.copy()
        sitio = get_current_site(request)
        cursite = Site.objects.get(pk=sitio.pk)
        pk = data.get('pk',None)
        parent = data.get('parent',None)
        sec_col_name = data.get('sec_colum_menu',None)
        if parent:
            sp = Section.objects.get(pk=parent)
            data['parent']=sp
        if sec_col_name:
            data['sec_colum_menu']=Seccolmenu.objects.get(pk=sec_col_name)
        
        responser = {}
        if pk:

            datos = {
                'sec_name':data['sec_name'],
                'sec_slug':slugify(data['sec_name'])
            }

            s = Section.objects.filter(pk=pk)
            s.update(**datos)
            
            responser['acts'] = True
            responser['msg'] = u'Registro guardado con éxito'
            responser['datos'] = {'pk':pk,
                                  'parent':parent,
                                  'sec_colum_menu':sec_col_name
                                  }

        else:
            datos = {}
            for x,y in data.items():
                datos[x]=y
            s = Section(**datos)
            s.sec_slug = slugify(datos['sec_name'])
            s.sitio = cursite
            s.save()

            responser['acts'] = True
            responser['msg'] = u'Registro guardado con éxito'
            responser['datos'] = {'pk':s.pk,
                                  'parent':parent,
                                  'sec_colum_menu':sec_col_name
                                  

                }


        return HttpResponse(simplejson.dumps(responser))


    def post(self,request):
        datapk = request.POST.get('pk',None)
        
        if datapk:
            s =  Rowsection.objects.get(pk=datapk)
            s.delete()
            self.context['removed']='ok'
            self.context['msg']=u'El elemento se removió con éxito'

        else:
            self.context['removed']='fail'
            self.context['msg']='Error, no fué posible remover el elemento'

        return HttpResponse(simplejson.dumps(self.context))

addSec = addSec.as_view()



'''

ADD COLUMN

'''

class addCol(View):

    context = {}
    
    def get(self,request):
        data = request.GET.copy()
        pk = data.get('pk',None)
        parent = data.get('parent',None)
        if parent:
            data['parent']=Section.objects.get(pk=parent)
        responser = {}
        if pk:

            datos = {
                'col_name':data['col_name'],
                'slug_col_name':slugify(data['col_name'])
            }

            s = Seccolmenu.objects.filter(pk=pk)
            s.update(**datos)
            
            responser['acts'] = True
            responser['datos'] = {'pk':pk,'sec_colum_menu':pk,'msg':'Registro Actualizado'}
        else:
            datos = {}
            for x,y in data.items():
                datos[x]=y
            s = Seccolmenu(**datos)
            s.slug_col_name = slugify(datos['col_name'])
            s.save()
            responser['msg'] = u'Registro guardado con éxito'
            responser['datos'] = {'pk':s.pk,'sec_colum_menu':s.pk}
        
        return HttpResponse(simplejson.dumps(responser))



addCol = addCol.as_view()


'''
/*   ROW ACTIONS ACTIONS*/
'''

class eddRowN(View):

    context = {}
    
    def get(self,request):
        data = request.GET.copy()
        pk = data.get('pk',None)
        if pk:
            r = Rowsection.objects.get(pk=pk)
            r.name_module = data['name_module']
            r.save()
            responder = {'acts':True,'msg':'Dato Actualizado con exito','cual':r.pk}
        else:
            responder = {'err':'error no se puedo realizar la operación :('}


        return HttpResponse(simplejson.dumps(responder))



eddRowN = eddRowN.as_view()


class rowReorder(View):
    def get(self,request):
        data = {}
        pks = request.GET.getlist('pks[]')
        for x in pks:
            orden = x.split('|')
            #data.append({'pk':orden[0],'orden':orden[1]})
            s = Rowsection.objects.get(pk=orden[0])
            s.orden = orden[1]
            s.save()

        data = {'success':'done','msg':'La estructura se modifico con éxito'}



        response = simplejson.dumps(data)
        return HttpResponse(response)

rowReorder = rowReorder.as_view()



class rowReorder(View):
    def get(self,request):
        data = {}
        pks = request.GET.getlist('pks[]')
        for x in pks:
            orden = x.split('|')
            #data.append({'pk':orden[0],'orden':orden[1]})
            s = Rowsection.objects.get(pk=orden[0])
            s.orden = orden[1]
            s.save()

        data = {'success':'done','msg':'La estructura se modifico con éxito'}



        response = simplejson.dumps(data)
        return HttpResponse(response)

rowReorder = rowReorder.as_view()



class rowRemover(View):
    def get(self,request):
        data = request.GET.copy()
        try: 
            r = Rowsection.objects.get(pk=data['pk'])
            r.delete()
            res = 'Eliminado con exito'
            responser = {'ok':res}
        except:
            responser = {'err':'error'}
       




        response = simplejson.dumps(responser)
        return HttpResponse(response)

rowRemover = rowRemover.as_view()




class rmModel(View):
    def get(self,request):
        step = request.GET.get('step',0)
        pk = request.GET.get('pk',None)
        modelos = [Linkmod,Section,Seccolmenu,User,Bancoimg,Mediasection,Rowsection,Videomodule,LinkDwn]
        responde = {}
        if pk:
            victim = modelos[int(step)]
            vict = victim.objects.get(pk=pk)
            vict.delete()
            responde = {'removed':'ok'}
        else:
            responde = {'wrong':'somthng works wrong, check  the bugger'}

        return HttpResponse(simplejson.dumps(responde))
rmModel = rmModel.as_view()



class chImage(View):
    
    def post(self,request):
        imagen = request.POST.get('webimage',None)
        pk = request.POST.get('pk',None)
        
        if pk and imagen:
            pads = '%s/static/links/headimage'%BASE_DIR
            nameimgs = '/static/links/headimage'
            imgx = imagen.decode('base64') 
            original = Image.open(BytesIO(imgx))
            name_imagen = '%s/%s_img.%s'%(pads,pk,original.format.lower())
            nameweb = '%s/%s_img.%s'%(nameimgs,pk,original.format.lower())
            if not os.path.exists(pads):
                os.makedirs(pads)

            webimage = open(name_imagen,'wb')
            webimage.write(imgx)
            webimage.close()
            sec = Section.objects.get(pk=pk)
            sec.webimage = nameweb
            sec.save()
            responde = {'pk':pk}
        else:
            responde = {'wrong':'somthng works wrong, check  the bugger'}

        return HttpResponse(simplejson.dumps(responde))
chImage = chImage.as_view()




class secPub(View):
    
    def get(self,request):
        pk = request.GET.get('pk',None)
        status = request.GET.get('status',False)
        columns = request.GET.get('columns',None)
        if pk:
            rw = Rowsection.objects.get(pk=pk)
            if columns:
                rw.configur=columns
                rw.save()

            publica = rw.linkmod_set.all()
            publica.update(publicado=True)

            publica = rw.textmodule_set.all()
            publica.update(publicado=True)

            publica = rw.mediasection_set.all()
            publica.update(publicado=True)


            publica = rw.videomodule_set.all()
            publica.update(publicado=True)


            publica = rw.bancoimg_set.all()
            publica.update(publicado=True)



            responde = {'updated':'ok'}
        else:
            responde = {'wrong':'somthng works wrong, check  the bugger'}

        return HttpResponse(simplejson.dumps(responde))
secPub = secPub.as_view()


class Downlods(View):
    
    def post(self,request):
        data = request.POST.copy()
        f = FormCreator()

        pk = data.get('pk',None)

        if pk:
            instanced = Downloade.objects.get(pk=pk)
        else:
            instanced = None


        forma = f.form_to_model(modelo=Downloade,excludes=['dfile'])
        forma = forma(data,instance=instanced)
        formats, imgstr = data['dfile'].split(';base64,')
        ext = formats.split('/')[-1]
        dfile = ContentFile(b64decode(imgstr), name=data['filename'])
        if forma.is_valid():
            saved = forma.save()
            saved.dfile = dfile
            saved.save()
            responde = {'saved':'ok','pk':'%s'%(saved.pk)}
        else:
            responde = {'wrong':forma.errors}

        return HttpResponse(simplejson.dumps(responde))
Downlods = Downlods.as_view()


class chLogo(View):
    def get(self,request):
        try:
            sec = Logo.objects.get(down_title='mainlogo')
            response = {'logo':sec.down_file}
        except:
            response = {'logo':'/static/imgs/logo.png'}

        return HttpResponse(simplejson.dumps(response))
    
    def post(self,request):
        imagen = request.POST.get('logofile',None)
        filename = request.POST.get('filename',None)

        
        if imagen:
            pads = '%s/static/imgs'%BASE_DIR
            nameimgs = '/static/imgs'
            imgx = imagen.decode('base64') 
            original = Image.open(BytesIO(imgx))
            name_imagen = '%s/%s'%(pads,filename)
            nameweb = '%s/%s'%(nameimgs,filename)
            webimage = open(name_imagen,'wb')
            webimage.write(imgx)
            webimage.close()
            sec,fail = Logo.objects.get_or_create(down_title='mainlogo')
            sec.down_file = nameweb
            sec.save()
            responde = {'pk':sec.pk}
        else:
            responde = {'wrong':'somthng works wrong, check  the bugger'}

        return HttpResponse(simplejson.dumps(responde))
chLogo = chLogo.as_view()

