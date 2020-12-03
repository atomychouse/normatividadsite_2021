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
from django.conf import settings


def checkuser(rq):
    #assert False,rq.user.groups.all()
    if not rq.user.groups.filter(name='admon').exists():
        return True
    else:
        return None    

class Index(View):
    template = 'admins/index.html'

    def get(self, request):

        pax = checkuser(request)
        if pax:
            return redirect('/home/')

        context = {}
        try:
            sitio = get_current_site(request)
            section = Section.objects.get(ishome=True,sitio=sitio)
            self.template = 'admins/main_templates/configurando.html'
        except:
            self.template = 'admins/index.html'
            section = None
        context = {}
        links = []
        context['section']=section
        context['sections']=Section.objects.filter(parent__isnull=True,sitio=sitio)

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

        selecte = request.GET.get('sel',None)
        papa = None
        columnapapa = None
        if selecte:
            try:
                selects = Section.objects.get(pk=selecte)
                papa = selects.parent.pk
                columnapapa = selects.sec_colum_menu.pk
            except:
                papa = None
                columnapapa = None

            if not papa:
                papa = selecte



        current_site = get_current_site(request)
        sectiones = []
        sections = Section.objects.filter(parent__isnull=True,sitio=current_site).order_by('orden')

        
        for stc in sections:

            if str(stc.pk)==str(papa):

                opened = 'true'
            else:
                opened = 'false'

            listado = {
                'pk':stc.pk,
                'sec_name':stc.sec_name,
                'sec_slug':stc.sec_slug,
                'page_type':stc.page_type,
                'ishome':stc.ishome,
                'opened':opened,
                'colpa':columnapapa,
                'ishome':stc.ishome,
                'cols':[{'cpk':c.pk,'opened':'true' if c.pk==columnapapa else 'false','col_name':c.col_name,'slug':c.slug_col_name,
                                'secs':[{
                                    'pk':sb.pk,
                                    'opened':'true' if str(sb.pk)==selecte else 'false',
                                    'sec_name':sb.sec_name,
                                    'sec_slug':sb.sec_slug,
                                    } for sb in c.section_set.all()]
                                } for c in stc.seccolmenu_set.all() ]        
            }

            '''
            plo = {
                    'pk':stc.pk,
                    'sec_name':stc.sec_name,
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
            '''
            sectiones.append(listado)
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
        pks = request.GET.getlist('pks[]')
        updateme = request.GET.get('updateme',None)
        typos = {'col':Seccolmenu,
                 'sec':Section
        }

        for x in pks:

            orden = x.split('|')

            modeli = typos[orden[2]]

            data.append({'pk':orden[0],'orden':orden[1]})
            s = modeli.objects.get(pk=orden[0])
            s.orden = orden[1]
            s.save()


        if updateme:
            ipk = request.GET.get('id',None)
            parent = request.GET.get('parent',None)
            orden = request.GET.get('orden',None)
            column = request.GET.get('column',None)
            mmodeli = request.GET.get('mymodeli','sec')
            mymodeli = typos[mmodeli]

            if column and column!='none':
                columna = column
            else:
                columna = None

            if mmodeli=='sec':
                data = {'parent':parent,
                        'orden':orden,
                        'sec_colum_menu':columna
                }
            else:
                data = {
                        'orden':orden,
                        'parent':parent
                }

            if not parent and modeli=='col':
                data = {'fail':'done','msg':'La estructura no es correcta'}

            else:    
                updating = mymodeli.objects.filter(pk=ipk)

                ups = updating.update(**data)

                data = {'success':'done','msg':'La estructura se modifico con éxito'}
            


        response = simplejson.dumps(data)
        return HttpResponse(response)


    def post(self, request):
        context = {}
        current_site = get_current_site(request)


        data = request.POST.copy()
        data['page_type'] = request.POST.get('page_type','homepage')        
        data['sec_slug'] = slugify(data['sec_name'])
        
        del data['csrfmiddlewaretoken']

        secol = data.get('sec_colum_menu',None)
        parent_pa = data.get('parent',None)


        if parent_pa:
            data['parent']=Section.objects.get(pk=parent_pa)
        else:
            data['parent'] = None

        if secol:
            data['sec_colum_menu']=Seccolmenu.objects.get(pk=data['sec_colum_menu'])
        else:
            del data['sec_colum_menu']

        pk = request.POST.get('pk',None)

        if pk:
            instanced = Section.objects.get(pk=pk)
        else:
            instanced = None
            #excludes = []

        if instanced:
            instanced.update(**data)
        else:
            datamod = {}
            for x,y in data.items():
                datamod[x]=y

            sitiop = Site.objects.get(pk=current_site.pk)
            s = Section(**datamod)
            s.sitio = sitiop
            s.save()
            

            instanced = s
        
        responde = {
                'saved':'ok',
                'datos':{'pk':instanced.pk,
                        
                         'mesagge':u'Sección Guardada con éxito',
                        },
                'callback':'reg_success'
            }
            
        return HttpResponse(simplejson.dumps(responde))            




     
addSection = addSection.as_view()


class Adminsection(View):
    template = ''
    def get(self,request,pk):
        checkuser(request)
        bancoimagen = request.GET.get('type',None)
        section = Section.objects.get(pk=pk)
        mod = request.GET.get('mod',None)
        if bancoimagen:
            section.page_type = bancoimagen
            section.save()

        #f = FormCreator()
        #forma = f.form_to_model(modelo=Section,excludes=['sec_slug','orden','parent','webimage','mobileimage','sitio'])
        #for x,y in forma.base_fields.iteritems():
        #    y.widget.attrs.update({'class':'lightinput'})
        #forma = forma(instance=section)
        #forma['sec_name'].field.widget.attrs.update({'ng-model':'sec_name'})
        #forma['page_type'].field.widget.attrs.update({'ng-model':'page_type'})
        if mod:
            contenido = Rowsection.objects.get(pk=mod)
        else:
            contenido = []

        template = 'admins/main_templates/configurando.html'
        context = {}
        links = []
        context['section']=section
        context['portada']=request.GET.get('portada',None)
        context['rw']=contenido
        context['ligas']=links
        context['cats'] = Cat.objects.filter(parentcat__isnull=True,secparent=section)
        context['sections']=Section.objects.filter(parent__isnull=True)

        response = render(request,template, context)
        return response
Adminsection = Adminsection.as_view()





class UploadB(View):
    def post(self,request):
        data = request.POST.copy()
        imagens = request.FILES.get('webimage',None)
        pk = data.get('pk',None)
        texto = data.get('texto','')
        recortar = data.get('recortar',False)


        rowpk = Rowsection.objects.get(pk=data['rowpk'])
        if pk:
            banco = Bancoimg.objects.get(pk=pk)               
        else:
            firstdata = {'texto':texto,'rowpk':rowpk}
            banco = Bancoimg(**firstdata)

        if imagens:
            #imagen = imagens.decode('base64') 
            original = Image.open(imagens)
            # EXTRACT SIXE AND CALCULATE WHO SIDE IS BEGER it
            wi = original.width
            hi = original.height
            if wi > hi:
                tw = 400.0
                recortew = 800.0
                th = (tw/wi) * hi
                recorteh = (recortew/wi) * hi
            else:                
                th = 400.0
                tw = (th/hi) * wi
                recorteh = 800.0
                recortew = (recorteh/hi) * wi
            recortesize = (int(recortew),int(recorteh)) 
            thumsize = (int(tw),int(th))
            thumb = original.resize(thumsize)
            recorte = original.resize(recortesize)
            name_imagen = 'banco.%s'%original.format.lower()
            data['webimage'] = imagens
            banco.recorte = imagens
            banco.original = imagens
            banco.webimage = data['webimage']                                
        banco.texto = texto
        banco.recortar = recortar
        banco.save()
        if imagens:
            thumb.save(banco.recorte.path)
            recorte.save(banco.webimage.path)
        
        response = {
                    'pk':banco.pk,'webimage':'%s'%(banco.webimage.name),
                    'texto':banco.texto,
                    'recortar':banco.recortar,
                    'orden':banco.orden
                    }

        return HttpResponse(simplejson.dumps(response))




UploadB = UploadB.as_view()



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
        descargar = request.POST.get('descargar',None)
        
        


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





        if pkid:

            instanced = modelo.objects.get(pk=pkid)
            
        else:
            instanced = None



        if instanced:
            rowupdate = instanced.rowpk
            rowupdate.configur = data['columns']
            rowupdate.save()

        #data['orden']=1

        if imagens:
            imagen = imagens.decode('base64') 
            original = Image.open(BytesIO(imagen))
            name_imagen = 'brouch.%s'%original.format.lower()
            data['webimage'] = ContentFile(imagen,name_imagen)

            
            if banco=='1':
                imagen = imagens.decode('base64') 
                imagen = Image.open(BytesIO(imagen))

                wi = original.width
                hi = original.height
                th = hi * 0.6 #200.0
                tw = (th/hi) * wi
                newsize = (int(tw),int(th))
                thimg = imagen.resize(newsize,Image.ANTIALIAS)
                img_str = thimg.tobytes()
                #img_str = img_str.decode('base64')
                name_imagen = 'websize.%s'%imagen.format.lower()
                data['originalfile'] = ContentFile(img_str,name_imagen)
            


        if smallimg:

            recortale = data.get('recortar',None)
            if recortale:
                imagen = smallimg.decode('base64') 
                original = Image.open(BytesIO(imagen))
                name_imagen = 'smallimage.%s'%original.format.lower()
                data['smallimage'] = ContentFile(imagen,name_imagen)
            else:

                wi = original.width
                hi = original.height
                th = 200.0
                tw = (th/hi) * wi
                newsize = (int(tw),int(th))
                thimg = imagen.resize(newsize,Image.ANTIALIAS)
                img_str = thimg.tobytes()
                #img_str = img_str.decode('base64')
                name_imagen = 'smallimage.%s'%imagen.format.lower()
                data['smallimage'] = ContentFile(img_str,name_imagen)



        if descargar:
            extt = request.POST.get('extt',None)
            formats, imgstr = descargar.split(';base64,')
            descargarextext = formats.split('/')
            namefile = 'bancoimg.%s'%(extt)
            data['descargar'] = ContentFile(b64decode(imgstr),name=namefile)



        f = FormCreator()



        forma = f.form_to_model(modelo=modelo,excludes=[])
        forma = forma(data,instance=instanced)
        if forma.is_valid():
            saved = forma.save()
            if imagens:
                saved.webimage = data['webimage']
                saved.save()

            if banco=='1':
                if descargar:
                    b = Bancodwfile(bancopk=saved,descargar=data['descargar'],extencion=extt,tipo=descargarextext[0])
                    b.save()

                    #saved.descargar = data['descargar']
                    #saved.save()

            
                try:
                    saved.recorte = data['originalfile']
                    saved.save()
                    thimg.save(saved.recorte.path)
                except:
                    pass


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
        modelos = [Section,Linkmod,Textmodule,'',Seccolmenu,Videomodule]
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
        modelos = [Linkmod,Section,None,Seccolmenu,User,Bancoimg,Mediasection,Rowsection,Videomodule,Downloade]
        responde = {}
        
        if pku:
            victim = modelos[int(step)]
            if int(step)==9:
                try:
                    vict = victim.objects.get(pk=pku)
                    vict.delete()
                except:
                    vict = LinkDwn.objects.get(pk=pku)
                    vict.delete()


            
            else:
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
        nodeses = request.GET.get('nodeses',[])
        orden = request.GET.get('orden',0)
        
        if not datapk:
            s =  Section.objects.get(pk=data['section'])
            if data['module']=='gridbanco':
                todos = s.rowsection_set.all()
                todos.update(publicado=False)
                s.page_type = 'bancoimagen'
                s.save()    
            rowinfo = {
                'sectionpk':s,
                'orden':orden,
                'module':data['module'],
                'name_module':data['name_module'],
                'configur':simplejson.dumps(nodeses)
            }
            nrow = Rowsection(**rowinfo)
            nrow.save()

            self.context['pk']=nrow.pk
            datos = {'pk':nrow.pk}

        return HttpResponse(simplejson.dumps(datos))

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
        secparent = request.GET.get('section',None)
        responsed = {}

        if secparent:
            sec = Section.objects.get(pk=secparent)
        else:
            sec = None

        if catname:
            catslug = slugify(catname)    
            data = {'catname':catname,'catslug':catslug,'secparent':sec}
            if parent:
                try:
                    data['parentcat']=Cat.objects.get(pk=parent)
                    catslug = '%s_%s'%(data['parentcat'].catname,catname)
                    data['catslug'] = slugify(catslug)
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



class rmCat(View):

    def get(self, request):
        pk = request.GET.get('pk',None)
        responsed = {}

        if pk:
            c = Cat.objects.get(pk=pk)
            c.delete()
            responsed['saved']='ok'
            responsed['pk']=pk
        else:
            responsed['fail']='nocat'

        response = HttpResponse(simplejson.dumps(responsed))
        return response

rmCat = rmCat.as_view()


class upCat(View):

    def get(self, request):
        pk = request.GET.get('pk',None)
        responsed = {}
        params = request.GET.copy()

        if pk:
            c = Cat.objects.get(pk=pk)
            
            if c.parentcat:
                sluger = '%s_%s'%(c.parentcat.catname,params['catname'])
                catslug = slugify(sluger)
            else:
                catslug = slugify(params['catname'])

            params['catslug']=catslug

            #c.delete()
            c.catname=params['catname']
            c.catslug = params['catslug']
            c.save()
            responsed['saved']='ok'
            responsed['pk']=pk
        else:
            responsed['fail']='nocat'

        response = HttpResponse(simplejson.dumps(responsed))
        return response

upCat = upCat.as_view()



class addDwnlink(View):

    def post(self, request):
        data = request.POST.copy()

        if data['sending']=='false':
            data['sending'] = False


        f = FormCreator()
        forma = f.form_to_model(modelo=Downloade,excludes=[])
        try:
            instanced = Downloade.objects.get(pk=data['pk'])
        except:
            instanced = None


        forma = forma(data,instance=instanced)

        if forma.is_valid():
            saved = forma.save()
            responsed = {'saved':'ok','pk':'%s'%(saved.pk),'dfile':instanced.dfile.name}
        else:
            errs = '%s'%(forma.errors) 
            responsed = {'errors':errs}

        response = HttpResponse(simplejson.dumps(responsed))
        return response

addDwnlink = addDwnlink.as_view()


class Rmbancofile(View):
    context = {}
    def post(self,request):
        checkuser(request)
        data = request.POST.copy()
        datapk = request.POST.get('pk',None)
        datos = {}
        if  datapk:
            b = Bancodwfile.objects.get(pk=datapk)
            b.delete()
            datos = {'pk':'removed'}

        return HttpResponse(simplejson.dumps(datos))

Rmbancofile = Rmbancofile.as_view()




class Videocvt(View):
    def get(self,request):
        context = {}
        template = 'admins/videocvt.html'
        videos = Videofiles.objects.all()
        context['vcvt'] = videos.filter(converted=True)
        context['vnocvt'] = videos.filter(converted=False)
        response = render(request,template, context)
        return response

Videocvt = Videocvt.as_view()



class upVideo(View):
    def post(self,request):
        response = {}
        data = request.POST.copy()
        archivo = request.FILES.get('file',None)
        v = Videofiles(**{'videof':archivo})
        v.save()
        response['saved']=v.pk
        response = simplejson.dumps(response)


        paths = 'cd %s & python manage.py videocvt'%(settings.BASE_DIR)
        os.system(paths)

        return HttpResponse(response)

    def get(self,request):
        context = {}
        template = 'admins/videocvt.html'

        response = render(request,template, context)
        return response

upVideo = upVideo.as_view()

