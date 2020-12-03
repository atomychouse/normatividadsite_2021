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


def checkuser(rq):
    #assert False,rq.user.groups.all()
    if not rq.user.groups.filter(name='admon').exists():
        return True
    else:
        return None    

class Index(View):
    template = 'doctor/index.html'

    def get(self, request):

        pax = checkuser(request)
        if pax:
            return redirect('/home/')

        context = {}
        try:
            sitio = get_current_site(request)
            section = Section.objects.get(ishome=True,sitio=sitio)
            self.template = 'doctor/main_templates/configuring.html'
        except:
            self.template = 'doctor/index.html'
            section = None
        context = {}
        links = []
        context['section']=section        
        response = render(request, self.template, context)
        return response

Index = Index.as_view()



class updateBlank(View):

    def post(self, request):
        rowpk = request.POST.get('rowpk',None)
        alto = request.POST.get('alto',120)
        r = Rowsection.objects.get(pk=rowpk)
        r.blankrow = alto
        r.save()

        context={'ok':r.blankrow}
        response = HttpResponse(simplejson.dumps(context))
        return response

updateBlank = updateBlank.as_view()

class IsHome(View):

    def post(self, request):
        CURRSITE = get_current_site(request)
        checkuser(request)
        context = {}
        pk = request.POST.get('sec',None)
        secs = Section.objects.filter(sitio=CURRSITE.pk)
        secs.update(ishome=False)
        if pk:
            sec = Section.objects.get(pk=pk)
            sec.ishome=True
            sec.sitio=CURRSITE
            sec.save()
            context = {'ishome':'ok'}
        else:
            context = {}

        response = HttpResponse(simplejson.dumps(context))
        return response

IsHome = IsHome.as_view()


class Seclist(View):
    template = ''
    def get(self,request):
        current_site = get_current_site(request)
        sectiones = []
        sections = Section.objects.filter(parent__isnull=True,sitio=current_site).order_by('orden')
        
        for stc in sections:

            plo = {
                    'pk':stc.pk,
                    'title':stc.sec_name,
                    'orden':stc.orden,
                    'nodes':[{'pk':x.pk,'title':x.sec_name,
                              'orden':x.orden,
                              'parent':x.parent.pk,
                              'nodes':[
                                {
                                    'pk':xx.pk,'title':xx.sec_name,
                                    'orden':xx.orden,
                                    'parent':xx.parent.pk
                                } for xx in x.section_set.all()
                              ]
                              } for x in stc.section_set.all()]
                        
            }

            sectiones.append(plo)
        return HttpResponse(simplejson.dumps(sectiones))

Seclist = Seclist.as_view()

#@method_decorator(login_required,name='addsection')



class UpdateSec(View):

    def post(self, request):
        context = {}
        current_site = get_current_site(request)
       
        data = request.POST.copy()
        data['page_type'] = request.POST.get('page_type','')        
        pk = request.POST.get('pk',None)
        if pk:
            instanced = Section.objects.get(pk=pk)
            instanced.sec_name = data['sec_name']
            instanced.sec_slug = slugify(data['sec_name'])
            
            
            instanced.save()
            
            excludes = []
            responde = {
                'saved':'ok',
                'datos':{'pk':instanced.pk,
                         'mesagge':u'Sección Guardada con éxito',
                        },
                'callback':'reg_success'
            }
            return HttpResponse(simplejson.dumps(responde))
        else:
            returner = {'errors':'error'}
            return HttpResponse(simplejson.dumps(returner))
     
UpdateSec = UpdateSec.as_view()




class addSection(View):
    def get(self,request):
        checkuser(request)
        response = {}
        data = []
        pks = request.GET.getlist('pks')
        for x in pks:
            orden = x.split('|')
            data.append({'pk':orden[0],'orden':orden[1]})
            s = Section.objects.get(pk=orden[0])
            s.orden = orden[1]
            s.save()
        response = simplejson.dumps(data)
        return HttpResponse(response)


    def post(self, request):
        context = {}
        current_site = get_current_site(request)
       
        data = request.POST.copy()
            
        data['page_type'] = request.POST.get('page_type','homepage')        
        pk = request.POST.get('pk',None)
        if pk:
            instanced = Section.objects.get(pk=pk)
            excludes = ['sec_slug','orden','parent','webimage','mobileimage']
        else:
            instanced = None
            excludes = []


        data['sec_slug']=slugify(data['sec_name'])
        data['sitio']=current_site.pk
        
        f = FormCreator()
        forma = f.form_to_model(modelo=Section,excludes=excludes)
        forma = forma(data,instance=instanced)

        if forma.is_valid():
            save_reg = forma.save()
            responde = {
                'saved':'ok',
                'datos':{'pk':save_reg.pk,
                         'mesagge':u'Sección Guardada con éxito',
                        },
                'callback':'reg_success'
            }
            
            return HttpResponse(simplejson.dumps(responde))
        else:
            returner = {'errors':forma.errors}
            return HttpResponse(simplejson.dumps(returner))
     
addSection = addSection.as_view()


class Adminsection(View):
    template = ''
    def get(self,request,pk):
        checkuser(request)

        bancoimagen = request.GET.get('type',None)


        section = Section.objects.get(pk=pk)
        
        if bancoimagen:
            section.page_type = bancoimagen
            section.save()

        f = FormCreator()
        forma = f.form_to_model(modelo=Section,excludes=['sec_slug','orden','parent','webimage','mobileimage','sitio'])
        for x,y in forma.base_fields.iteritems():
            y.widget.attrs.update({'class':'lightinput'})
        forma = forma(instance=section)
        forma['sec_name'].field.widget.attrs.update({'ng-model':'sec_name'})
        forma['page_type'].field.widget.attrs.update({'ng-model':'page_type'})
        

        template = 'doctor/main_templates/configuring.html'
        context = {}
        links = []
        context['section']=section
        context['forma']=forma
        context['ligas']=links
        context['cats'] = Cat.objects.filter(parentcat__isnull=True)
        response = render(request,template, context)
        return response
Adminsection = Adminsection.as_view()




class SaveMedia(View):

    def post(self,request):
        response = {}
        data = request.POST.copy()
        imagens = request.POST.get('webimage',None)
        smallimg = request.POST.get('smallimg',None)
        pkid = request.POST.get('pkid',None)
        rowpk = request.POST.get('rowpk',None)
        banco = request.POST.get('banco',0)
        cats = request.POST.getlist('cats[]')
        

        data['cats']=simplejson.dumps(cats)

        modelos = [Mediasection,Bancoimg]
        modelo = modelos[int(banco)]

        flotando = request.POST.get('flotando',None)
        invflotando = request.POST.get('invflotando',None)
        imagesize = request.POST.get('imagesize',6)
        textsize = request.POST.get('textsize',6)

        if flotando and invflotando:
            configures = {
                          'flotando':flotando,
                          'invflotando':invflotando,
                          'imagesize':imagesize,
                          'textsize':textsize
                          }
            configures = simplejson.dumps([configures])
            data['configs'] = configures



        if rowpk:
            rowupdate = Rowsection.objects.get(pk=rowpk)
            rowupdate.configur = data['columns']
            rowupdate.save()

        if pkid:

            instanced = modelo.objects.get(pk=pkid)
            
        else:
            instanced = None


        #data['orden']=1

        if imagens:
            imagen = imagens.decode('base64') 
            original = Image.open(BytesIO(imagen))
            name_imagen = 'brouch.%s'%original.format.lower()
            data['webimage'] = ContentFile(imagen,name_imagen)


        if smallimg:
            imagen = smallimg.decode('base64') 
            original = Image.open(BytesIO(imagen))
            name_imagen = '%s'%original.format.lower()
            data['smallimage'] = ContentFile(imagen,name_imagen)


        f = FormCreator()



        forma = f.form_to_model(modelo=modelo,excludes=[])
        forma = forma(data,instance=instanced)
        if forma.is_valid():
            saved = forma.save()
            if imagens:
                saved.webimage = data['webimage']
                saved.save()
            if smallimg:
                saved.smallimage = data['smallimage']
                saved.save()

            response = {'pk':saved.pk}
        else:
            response = forma.errors


        return HttpResponse(simplejson.dumps(response))

SaveMedia = SaveMedia.as_view()




class SaveDwn(View):

    def post(self,request):
        assert False,'done'
        response = {}
        data = request.POST.copy()
        imagens = request.POST.get('webimage',None)
        pkid = request.POST.get('pkid',None)
        rowpk = request.POST.get('rowpk',None)

        if rowpk:
            rowupdate = Rowsection.objects.get(pk=rowpk)
            rowupdate.configur = data['columns']
            rowupdate.save()

        if pkid:
            instanced = Mediasection.objects.get(pk=pkid)
            
        else:
            instanced = None


        data['orden']=1
        if imagens:
            imagen = imagens.decode('base64') 
            original = Image.open(BytesIO(imagen))
            name_imagen = 'brouch.%s'%original.format.lower()
            data['webimage'] = ContentFile(imagen,name_imagen)
        f = FormCreator()
        forma = f.form_to_model(modelo=Mediasection,excludes=[])
        forma = forma(data,instance=instanced)
        if forma.is_valid():
            saved = forma.save()
            if imagens:
                saved.webimage = data['webimage']
                saved.save()

            response = {'pk':saved.pk}
        else:
            response = forma.errors


        return HttpResponse(simplejson.dumps(response))

SaveDwn = SaveDwn.as_view()

class SaveModel(View):
    def post(self,request):

        retorno = []
        modelos = [Section,Linkmod,Textmodule,Secrowmenu,Seccolmenu,Videomodule]
        data = request.POST.copy()
        modelo = modelos[int(data['step'])]
        imagens = request.POST.get('imagen',None)
        pkid = request.POST.get('pkid',None)
        sec_name = request.POST.get('sec_name',None)
        col_name = request.POST.get('col_name',None)
        texto = request.POST.get('texto',None)
        

        
        current_site = get_current_site(request)
        data['sitio']=current_site.pk

        #if texto:
        #    data['texto'] = texto.replace("'","\'")
        #    data['texto'] = data['texto'].replace('&#39;','\&#39;')
            

        # se esta  recibiendo una seccion, vamos a generar su slug
        if sec_name and int(data['step'])==0:
            data['sec_slug']=slugify(sec_name)

        if col_name and int(data['step'])==4:
            data['slug_col_name']=slugify(col_name)


        
        rowpk = request.POST.get('rowpk',None)

        if rowpk and int(data['step'])!=4:
            rowupdate = Rowsection.objects.get(pk=rowpk)
            rowupdate.configur = data['columns']
            rowupdate.save()
        
        
        if pkid:
            instanced = modelo.objects.get(pk=pkid)
        else:
            instanced = None

        if imagens:
            imagen = data['imagen'].decode('base64') 
            original = Image.open(BytesIO(imagen))
            name_imagen = 'brouch.%s'%original.format.lower()
            data['imagen'] = ContentFile(imagen,name_imagen)
        else:
            data['imagen']=None
        
        f = FormCreator()
        forma = f.form_to_model(modelo=modelo,excludes={})
        forma = forma(data,instance=instanced)
        if forma.is_valid():
            saved = forma.save()
            if data['imagen']:
                saved.imagen = data['imagen']
                saved.save()
            retorno = {'saved':'ok','pk':saved.pk}
        else:
            retorno = forma.errors

        response = HttpResponse(simplejson.dumps(retorno))
        return response
SaveModel = SaveModel.as_view()




class Delmodel(View):
    def post(self,request):
        step = request.POST.get('step',0)
        pku = request.POST.get('pku',None)
        modelos = [Linkmod,Section,Secrowmenu,Seccolmenu,User,Bancoimg,Mediasection,Rowsection,Videomodule,LinkDwn]
        responde = {}
        if pku:
            victim = modelos[int(step)]
            vict = victim.objects.get(pk=pku)
            vict.delete()
            responde = {'removed':'ok'}
        else:
            responde = {'wrong':'somthng works wrong, check  the bugger'}
        return HttpResponse(simplejson.dumps(responde))
Delmodel = Delmodel.as_view()


class addRow(View):
    context = {}
    def get(self,request):
        checkuser(request)
        data = request.GET.copy()
        datapk = request.GET.get('pk',None)
        orden = request.GET.get('orden',0)
        if not datapk:
            s =  Section.objects.get(pk=data['section'])
            rowinfo = {
                'sectionpk':s,
                'orden':orden,
                'module':data['module'],
                'name_module':data['name_module'],
                'configur':simplejson.dumps(data['nodeses'])
            }
            nrow = Rowsection(**rowinfo)
            nrow.save()

            self.context['pk']=nrow.pk

        return HttpResponse(simplejson.dumps(self.context))

addRow = addRow.as_view()


class rmRow(View):
    context = {}
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

rmRow = rmRow.as_view()


class reorderVw(View):
    def get(self, request):
        data = request.GET.getlist('pk')
        try: 
            for i in data:
                pices = i.split('|')
                r = Rowsection.objects.get(pk=pices[0])
                r.orden = pices[1]
                r.save()

            response = HttpResponse(simplejson.dumps({'msg':'El orden se actualizó correctamente'}))
            return response
        except:
            response = HttpResponse(simplejson.dumps({'msg':'something is wrong :('}))
            return response

reorderVw = reorderVw.as_view()


class AddFile(View):
    def post(self, request):
        data = request.POST.copy()
        f =  FormCreator()
        forma = f.form_to_model(modelo=Downloadmod,excludes=[])
        forma = forma(data,request.FILES)

        if forma.is_valid():
            saved = forma.save()
            response = HttpResponse(simplejson.dumps({'path':'/%s'%saved.dwfile.url}))
            return response
        else:
            response = HttpResponse(simplejson.dumps({'msg':'something is wrong :(','err':forma.errors}))
            return response



AddFile = AddFile.as_view()



# REMOVING FILE

class delFile(View):
    def get(self,request):
        responde = {}

        filename = request.GET.get('filename',None)
        if filename:
            #searchfilename = 'static/downlobles/%s'%filename
            f = Downloadmod.objects.get(pk=filename)
            os.remove(f.dwfile.path)
            f.delete()
            responde['ok']='deleted'
        else:
            responde['error']='some fucking error ocurre. >:s'

        return HttpResponse(simplejson.dumps(responde))
delFile = delFile.as_view()

'''
CATEGORY ADMINISTRATION
'''


class addCat(View):

    def get(self, request):
        catname = request.GET.get('catname',None)
        parent = request.GET.get('parent',None)
        responsed = {}

        if catname:
            catslug = slugify(catname)    
            data = {'catname':catname,'catslug':catslug}
            if parent:
                try:
                    data['parentcat']=Cat.objects.get(pk=parent)
                except:
                    pass

            ncat = Cat(**data)
            ncat.save()
            responsed['saved']='ok'
            responsed['pk']=ncat.pk
        else:
            responsed['fail']='nocat'

        response = HttpResponse(simplejson.dumps(responsed))
        return response

addCat = addCat.as_view()


class addDwnlink(View):

    def post(self, request):
        data = request.POST.copy()
        f = FormCreator()
        forma = f.form_to_model(modelo=LinkDwn,excludes=[])
        try:
            instanced = LinkDwn.objects.get(pk=data['pk'])
        except:
            instanced = None

        forma = forma(data,instance=instanced)

        if forma.is_valid():
            saved = forma.save()
            responsed = {'saved':'ok','pk':saved.pk}
        else:
            errs = '%s'%(forma.errors) 
            responsed = {'errors':errs}

        response = HttpResponse(simplejson.dumps(responsed))
        return response

addDwnlink = addDwnlink.as_view()