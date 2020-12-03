# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template.context import RequestContext
from django.views.generic import View
from django.contrib.auth.models import User,Group
from rudimentario.modelforms import FormCreator
from django import forms
import simplejson
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, BadHeaderError
from rudimentario.settings import EMAIL_HOST
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError
from doctor.models import * 
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.defaultfilters import slugify
import time
import os
from django.conf import settings
import mimetypes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from campainsapp.models import * 
from django.http import JsonResponse
from django.core.paginator import Paginator


class Seclist(View):
    template = ''
    def get(self,request):

        current_site = get_current_site(request)

        try:
            sections_pks = request.user.groups.all()[0].permission_set.all()[0].permslist()
            #sections_pks = simplejson.loads(sections_pks.permisos)
            sections_all = Section.objects.filter(pk__in=sections_pks,ishome=False)
        except:
            sections_pks = None
            sections_all = []


        papas = []
        for x in sections_all:
            try: 
                papi = x.parent.pk
            except:
                papi = x.pk
            if not papi in papas:
                papas.append(papi)


        sectiones = []
        if sections_pks:
            searchs_all = {'pk__in':sections_pks,'ishome':False}
        else:
            searchs_all = {'ishome':False}

        if len(papas)>0:
            searchs = {'pk__in':papas}
        else:
            searchs = {}

        sections = Section.objects.filter(parent__isnull=True,ishome=False,sitio=current_site,**searchs).order_by('orden')        
        for stc in sections:
            plo = {
                    'pk':stc.pk,
                    'sec_name':stc.sec_name,
                    'sec_slug':stc.sec_slug,
                    'mobileimage':stc.mobileimage,
                    'webimage':stc.webimage,
                    'orden':stc.orden,
                    'cols':[
                                {
                                    'pk':xx.pk,
                                    'col_name':xx.col_name,
                                    's_col_name':xx.slug_col_name,
                                    'orden':xx.orden,
                                    'secs':[
                                        {
                                        'pk':sec_col.pk,
                                        'sec_name':sec_col.sec_name,
                                         'sec_slug':sec_col.sec_slug
                                        } 
                                        for sec_col in xx.section_set.filter(**searchs_all)
                                    ]
                                } for xx in stc.seccolmenu_set.all()
                    ]
                        
                }

            sectiones.append(plo)

        staticsec = {
                    'pk':0,
                    'sec_name':'Campañas',
                    'sec_slug':'campanyas',
                    'mobileimage':"/static/links/headimage/147829221738_small.jpeg",
                    'webimage':"/static/links/headimage/147829221738_small.jpeg",
                    'orden':6,
                    'cols':[]
        }

        sectiones.append(staticsec)
        return HttpResponse(simplejson.dumps(sectiones))

Seclist = Seclist.as_view()



class AllSeclist(View):
    template = ''
    def get(self,request):

        current_site = get_current_site(request)

        try:
            sections_pks = request.user.groups.all()[0].permission_set.all()[0].permslist()
            #sections_pks = simplejson.loads(sections_pks.permisos)
            sections_all = Section.objects.filter(pk__in=sections_pks,ishome=False)
        except:
            sections_pks = None
            sections_all = []

        papas = []
        for x in sections_all:
            try: 
                papi = x.parent.pk
            except:
                papi = x.pk
            if not papi in papas:
                papas.append(papi)


        sectiones = []
        if sections_pks:
            searchs_all = {'pk__in':sections_pks,'ishome':False}
        else:
            searchs_all = {'ishome':False}

        if len(papas)>0:
            searchs = {'pk__in':papas}
        else:
            searchs = {}

        sections = Section.objects.filter(parent__isnull=True,sitio=current_site,**searchs).order_by('orden')        
        for stc in sections:
            plo = {
                    'pk':stc.pk,
                    'sec_name':stc.sec_name,
                    'sec_slug':stc.sec_slug,
                    'mobileimage':stc.mobileimage,
                    'webimage':stc.webimage,
                    'orden':stc.orden,
                    'cols':[
                                {
                                    'pk':xx.pk,
                                    'col_name':xx.col_name,
                                    's_col_name':xx.slug_col_name,
                                    'orden':xx.orden,
                                    'secs':[
                                        {
                                        'pk':sec_col.pk,
                                        'sec_name':sec_col.sec_name,
                                         'sec_slug':sec_col.sec_slug
                                        } 
                                        for sec_col in xx.section_set.filter(**searchs_all)
                                    ]
                                } for xx in stc.seccolmenu_set.all()
                    ]
                        
                }

            sectiones.append(plo)

        staticsec = {
                    'pk':0,
                    'sec_name':'Campañas ss',
                    'sec_slug':'campanyas',
                    'mobileimage':"/static/links/headimage/147829221738_small.jpeg",
                    'webimage':"/static/links/headimage/147829221738_small.jpeg",
                    'orden':14,
                    'cols':[]
        }

        sectiones.append(staticsec)


        return HttpResponse(simplejson.dumps(sectiones))

AllSeclist = AllSeclist.as_view()



class Index(View):
    template = 'mainapp/index.html'

    def get(self, request):

        logout_pass = request.GET.get('logout',None)
        
        if logout_pass:
            logout(request)

        if request.user.is_active:
            if 'admon' in request.user.groups.all():

                if u'campañas' in request.user.groups.all():
                    response = redirect("/campains/")
                else:
                    response = redirect("/admin/")

                return response
            else:
                response = redirect("/home/")
                return response

        context = {}
        forma = FormCreator()
        widgets = {
            'password':forms.PasswordInput(),
        }

        forma = forma.form_to_model(modelo=User,
                                             fields=['username','password','first_name','last_name','email'],
                                             widgets = widgets
                                             )
        for x,y in forma.base_fields.iteritems():
            (y.widget.attrs.update({'class':'form-control'}))

        context['forma'] = forma

        response = render(request, self.template, context)
        return response

Index = Index.as_view()


class Home(View):
    template = 'mainapp/inicio.html'
    def get(self,request):
        context = {}
        current_site = get_current_site(request)

        try:


            permiso = request.user.groups.filter(name='admon').exists()
            if permiso:
                perms = []
            else:
                perms = request.user.groups.all()[0].permission_set.all()[0]
                perms = perms.permslist()
            sechome = Section.objects.get(ishome=True,sitio=current_site)
            
            if sechome.pk in perms or permiso:
                sechome = sechome

            else:
                sechome = Section.objects.get(pk=perms[0],sitio=current_site)




            context['section']=sechome
            self.template = 'mainapp/config.html'
            firstvideo = sechome.rowsection_set.filter(module='video')
            
            if firstvideo.count() > 0 :
                firstvideopk = firstvideo[0].videomodule_set.all()[0].videoid
                context['fv']=firstvideopk
        except:
            sechome = None



        if sechome and sechome.page_type=='bancoimagen':
            context['cats']=Cat.objects.filter(parentcat__isnull=True)


        response = render(request, self.template, context)
        return response


Home = Home.as_view()




class Sin(View):

    def post(self,request):
        data = request.POST.copy()
        user = authenticate(username=data['usuarius'], password=data['passo'])
        response = {}
        
        try:
            group = user.groups.values()[0]['name']
        except:
            
            group = 'basic'

        if user is not None:
            login(request, user)
            response['saved'] = 'ok'
            response['datos'] = {'msg':u'guardao con éxito','liga':'/admin/'}
            response['callback'] = 'reg_success'
        else:
            response['msg'] = 'la información no es correcta, verifique por favor'
            response['errors'] = {'usuarius':'Usuario no es correcto'}

        return HttpResponse(simplejson.dumps(response))


Sin = Sin.as_view()


class Son(View):

    def post(self,request):
        data = request.POST.copy()
        data['date_joined'] = datetime.datetime.now()
        instanced = None
        response = {}
        forma = FormCreator()
        forma = forma.advanced_form_to_model(modelo=User,
                                             excludes = []
                                             )

        forma.base_fields['email'].required=True
        forma.base_fields['groups'].required=True
        grupo = data['groups']
        ges = Group.objects.get(name='%s'%data['groups'])
        data['groups'] = (ges.pk)
        data['is_active']=True
        data['is_staff']=True
        pax = data['password']
        data['password']=make_password(data['password'])
        forma = forma(data,instance=instanced)

        if forma.is_valid():
            saved = forma.save()
            if data['groups']=='patient':
                full_name = '%s %s' %(data['first_name'],data['last_name'])
                Patient(full_name='')
            if saved:
                usery = authenticate(username=data['username'], password=pax)
                login(request, usery)


            response['saved'] = 'ok'
            response['datos'] = {'msg':u'guardao con éxito','liga':'/%s/home/'%(grupo)}
            response['callback'] = 'reg_success'

        else:
            response['msg'] = 'Verifique su información'
            response['errors'] = forma.errors


        returns = HttpResponse(simplejson.dumps(response))
        
        return returns

Son = Son.as_view()




class Udetail(View):
    """Delete company."""
    template = 'mainapp/config.html'

    def get(self,request,section=None,column=None,subsection=None):



        if 'campanyas' in subsection:
            response = redirect("/campanyas/")
            return response



        permiso = request.user.groups.filter(name='admon').exists()

        if permiso:
            sections_pks = []
        else:
            sections_pks = request.user.groups.all()[0].permission_set.all()[0]
            sections_pks = simplejson.loads(sections_pks.permisos)
        
        xx = [int(x) for x in sections_pks]

        context = {}
        searchs = {'sec_slug':subsection,'sec_colum_menu__isnull':True}
        #if secty:
        #    searchs['parent__sec_slug']=secty
        
        main_section_filter = {}

        if section:
            main_section_filter['parent__sec_slug']=section
        if column:
            main_section_filter['sec_colum_menu__slug_col_name']=column
        if subsection:
            main_section_filter['sec_slug']=subsection


        if column:
            section = Section.objects.get(**main_section_filter)
        else:
            section = Section.objects.get(**searchs)


        if section.pk in xx or permiso:            
            context['section']=section
            firstvideo = section.rowsection_set.filter(module='video')
            if firstvideo.count() > 0 :
                firstvideopk = firstvideo[0].videomodule_set.all()[0].videoid
                context['fv']=firstvideopk
            #context['sections']=Section.objects.filter(parent__isnull=True)
                
        else:
            self.template = 'mainapp/nopermisos.html'


        if section.page_type in ['bancoimagen'] :
            context['cats'] = Cat.objects.filter(parentcat__isnull=True,secparent=section)


        response = render(request, self.template, context)
        return response

Udetail = Udetail.as_view()



class Crop(View):
    @csrf_exempt
    def post(self,request):
        tipo = request.POST.get('tipo',1)
        portal = request.POST.get('portal',1)
        sectionpk = request.POST.get('uid',None)
        uid =slugify(time.time())

    #   setting_dirs -----------------------------------------------------
        if not os.path.exists("%s/static/%s/"%(settings.BASE_DIR,portal)):
            os.mkdir("%s/static/%s/"%(settings.BASE_DIR,portal))
        if not os.path.exists("%s/static/%s/%s/"%(settings.BASE_DIR,portal,tipo)):
            os.mkdir("%s/static/%s/%s/"%(settings.BASE_DIR,portal,tipo))
        
    #   crop procecing---------------------------------------------------

        #calling libs ---------------------------------------------------
        from PIL import Image
        from io import BytesIO

        #image params --------------------------------------------
        filefi = '%s'%request.POST.get('imgUrl',None)

        filefi = filefi.decode('base64')    
        
        #creating a image-----------------------------------------------------
        original = Image.open(BytesIO(filefi))


        #cropping data--------------------------------------------------------
        data = request.POST.copy()
        x1 = int(float(data['imgX1'])) 
        y1 = int(float(data['imgY1']))
        x2 = int(float(data['cropW'])) + x1 
        y2 = int(float(data['cropH'])) + y1
        w = int(float(data['imgW']))
        h = int(float(data['imgH']))
        basewidth = 320        
        box = (x1,y1,x2,y2)
        resizing = original.resize((w,h),Image.ANTIALIAS)
        cropped = resizing.crop(box)
        originalW = float(cropped.size[0])
        originalH = float(cropped.size[1])
        wxpercent = basewidth  / originalW
        hsize = float(originalH) * float(wxpercent)
        hsize = int(hsize)
        mobile = cropped.resize((basewidth,hsize),Image.ANTIALIAS)

        nameImage = '%s/static/%s/%s/%s.%s'%(settings.BASE_DIR,portal,tipo,uid,original.format.lower())
        nameimagedb = '/static/%s/%s/%s.%s'%(portal,tipo,uid,original.format.lower())
        mobilName = '%s/static/%s/%s/%s_small.%s'%(settings.BASE_DIR,portal,tipo,uid,original.format.lower())
        mobilNamedb = '/static/%s/%s/%s_small.%s'%(portal,tipo,uid,original.format.lower())
        
        cropped.save(nameImage,original.format)
        mobile.save(mobilName,original.format)
        

        if sectionpk:
            s = Section.objects.get(pk=sectionpk)
            s.webimage  = nameimagedb
            s.mobileimage = mobilNamedb
            s.save()
        
        #es.indices.refresh(index='gdata34')
        response = {"status":"success",'uids':uid,
                    "url":'%s'%(nameimagedb)}
        response = simplejson.dumps(response)

        return HttpResponse(response)

Crop = Crop.as_view()


class Download(View):

    def get(self,request):
        filekey = request.GET.get('f',None)

        fpk = request.GET.get('fpk',None)
        if fpk:
            fikey = Downloadmod.objects.pk(pk=fpk)
            filey = fikey.dwfile.name.split('/')
            filekey = '%s'%filey[-1:][0]



        if 'static' not in filekey:
            filekey = 'static/downlobles/%s'%filekey #assert False,'ok'

        

        filename = '%s/%s'%(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),filekey)
        
        mm = mimetypes.guess_extension(filename)
        mtype = mimetypes.guess_type(filename)
        downloadame,extension = os.path.splitext(filename)
        datename = '%s'%datetime.datetime.now()
        nuname = '%s%s'%(slugify(datename),extension)
        f = open(filename)
        response = HttpResponse(f,content_type=mtype[0])

        dname_list = downloadame.split('/')
        dname = dname_list[len(dname_list)-1]

        response['Content-Disposition'] = 'attachment; filename="%s%s"'%(dname,extension)
        return response
Download = Download.as_view()



class Sender(View):

    def post(self,request):
        current_site = get_current_site(request)
        data = request.POST.copy()
        urix = '%s/dw/?f=%s'%(current_site,data['fileid'])

        subject, from_email, to = 'Archivo compartido', 'claro@normatividadclaro.com',data['correo_envio']

        mensaje = u'''
            <h1>Hola : %s</h1>
            <p>%s te ha enviado un archivo de Normatividad Claro. </p>
            <p><a href="%s">Descargar</a></p>

        '''%(data['nombre_envio'],request.user.first_name,urix)


        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, mensaje, from_email, [to])
        msg.attach_alternative(mensaje, "text/html")
        msg.send()

        return HttpResponse(urix)


Sender = Sender.as_view()




class Camps(View):
    template = 'mainapp/camps.html'
    def get(self,request):
        context = {}
        reds = Campanya.objects.all().exclude(statusfile='pendiente').order_by('-id')
        cabecera = Pageinfo.objects.all().first()#None #request.user.campanya_set.filter(typofile__icontains='image').exclude(statusfile='pendiente').order_by('?').first()
        cats = Campaincat.objects.filter(parentcat__isnull=True)
        readys = []
        videos_abalible = []
        for r in reds:
            
            if 'image' in r.typofile:

                item = {
                    'pk':r.pk,
                    'mini':r.campanyafile_set.filter(typofile='mini').first().itemfile.url,
                    'desktop':r.campanyafile_set.filter(typofile='desktop').first().itemfile.url,
                    'original':r.original.url,
                    'titulo':r.titulo,
                    'typofile':r.typofile,
                    'datatarget':'cp_lightbox',
                    'mycats':r.mycats()
                }

            else:

                item = {
                    'pk':r.pk,
                    'mini':'static/campains_crops/%s_tb.jpg'%(r.pk),
                    'desktop':'',
                    'original':r.original,
                    'titulo':r.titulo,
                    'typofile':r.typofile,
                    'datatarget':'cp_videobox',
                    'mycats':r.mycats()
                }

            readys.append(item)



        if cabecera:
            head_img = cabecera.imagen.url
        else:
            head_img = ''
            
        context = {
                'readys':readys,
                'videos':videos_abalible,
                'head':head_img,
                'cats':cats,
                'groups':[x.name for x in request.user.groups.all()]
            }
            


        response = render(request, self.template, context)
        return response


Camps = Camps.as_view()







class listCamps(View):
    template = 'mainapp/camps.html'
    def get(self,request):
        context = {}
        readys = []
        page = request.GET.get('page',1)
        cats = request.GET.getlist('cats',None)
        orden = request.GET.get('orden',"-id")
	if orden == '-id':
		orden = ('anyo_display','mes_display')
        else:
                orden = ('-anyo_display','-mes_display')
        if cats:
            #reds = Campanya.objects.filter(campcat__categoria__in=cats).exclude(statusfile='pendiente').order_by(*orden)
	    reds = Campanya.objects.all().exclude(statusfile='pendiente').order_by(*orden)
            for c in cats:
                reds = reds.filter(campcat__categoria_id=c)

        else:
            reds = Campanya.objects.all().exclude(statusfile='pendiente').order_by(*orden)
        filtro = request.GET.get('filtro',None)
        if filtro:
    	    if 'status_' in filtro:
                reds = reds.filter(statuscamp__icontains=request.GET.get('filtro'))
            else:
                reds = reds.filter(typofile__icontains=request.GET.get('filtro'),statuscamp__icontains='status_activado')
                #assert False,request.GET.get('filtro')

        if request.GET.get('destacado',None):
            reds = reds.filter(destacado=True)
        currpage = Paginator(reds,12)
        pageobj = currpage.page(page)
        pagelist = pageobj.object_list
        for r in pagelist:
            titulo = r.titulo
            if len(r.titulo)<3:
                cats = [x['namecat'] for x in r.jsoncats()]
                titulo = ' '.join(cats)
            if 'image' in r.typofile:
                item = {
                    'pk':r.pk,
                    'a':len(r.titulo),
                    'cats':cats,
                    'mini':'/%s'%r.campanyafile_set.filter(typofile='mini').first().itemfile.url,
                    'desktop':'/%s'%r.campanyafile_set.filter(typofile='desktop').first().itemfile.url,
                    'original':'/%s'%r.original.url,
                    'titulo':titulo,
                    'atachs':r.myattachs(),
                    'typofile':r.typofile.split('/')[0],
                    'datatarget':'cp_lightbox',
                    'mycats':r.jsoncats()
                }
            else:
                item = {
                    'pk':r.pk,
                    'a':len(r.titulo),
                    'mini':'/static/campains_crops/%s_tb.jpg'%(r.pk),
                    'desktop':'',
                    'original':'/%s'%r.original.url,
                    'titulo':titulo,
                    'atachs':r.myattachs(),
                    'typofile':r.typofile.split('/')[0],
                    'datatarget':'cp_videobox',
                    'mycats':r.jsoncats()
                }
            readys.append(item)
            
        context = {
                'readys':readys,
                'pages':currpage.num_pages
            }

        response = JsonResponse(context,safe=False)
        return response


listCamps = listCamps.as_view()
