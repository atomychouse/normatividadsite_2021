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
from rudimentario.modelforms import FormCreator
from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from doctor.views import checkuser
from django.core.mail import send_mail, EmailMessage
from django.core.mail import send_mass_mail
from django.core.mail import get_connection, EmailMultiAlternatives


class userForm(View):
    template = 'admins/user.html'


    def get(self,request):

        pax = checkuser(request)
        if pax:
            return redirect('/home/')


        context = {}
        forma = FormCreator()
        pk = request.POST.get('pk',None)


        if pk:
            instanced = User.objects.get(pk=pk)
            permisos = instanced.permission_set.all()[0]
            permisos = permisos.permslist()
        else:
            instanced = None
            permisos = []


        widgets = {
            'password':forms.PasswordInput(),
            'groups':forms.Select()
        }

        forma = forma.form_to_model(modelo=User,
                                             fields=['username','password','first_name','last_name','email','groups'],
                                             widgets = widgets
                                             )
        for x,y in forma.base_fields.iteritems():
            (y.widget.attrs.update({'class':'form-control'}))


        forma = forma(instance=instanced)

        sections = None     


        context['forma'] = forma
        context['pk'] = pk
        context['sections'] = sections
        context['permisos'] = permisos
        context['grupos'] = Group.objects.all().order_by('name')

        response = render(request, self.template, context)
        return response

    def post(self,request):

        pax = checkuser(request)
        if pax:
            return redirect('/home/')


        context = {}
        forma = FormCreator()
        pk = request.POST.get('pk',None)


        if pk:
            instanced = User.objects.get(pk=pk)
            permisos = instanced.groups.all()[0].permission_set.all()
            if permisos:
                permisos = permisos[0].permslist()
        else:
            instanced = None
            permisos = []




        widgets = {
            'password':forms.PasswordInput(),
            'groups':forms.Select()
        }


        forma = forma.form_to_model(modelo=User,
                                             fields=['username','password','first_name','last_name','email','groups'],
                                             widgets = widgets
                                             )
        for x,y in forma.base_fields.iteritems():
            (y.widget.attrs.update({'class':'form-control'}))


        forma = forma(instance=instanced)

        sections = Section.objects.filter(parent__isnull=True,ishome=False).order_by('orden')        


        context['forma'] = forma
        context['users'] = User.objects.all()
        context['pk'] = pk
        context['sections'] = sections
        context['permisos'] = permisos
        context['grupos'] = Group.objects.all().order_by('name')

        response = render(request, self.template, context)
        return response

userForm = userForm.as_view()


class Son(View):
    template = 'admins/users.html'
    def get(self,request):
        
        pax = checkuser(request)
        if pax:
            return redirect('/home/')

        context = {}

        context['users'] = User.objects.all()
        context['grupos'] = Group.objects.all().order_by('name')

        response = render(request, self.template, context)
        return response
        


    def post(self,request):
        data = request.POST.copy()
        passs = request.POST.get('password',None)
        pk = request.POST.get('pk',None)
        group = request.POST.get('groups',None)
        
        if group:
            data['groups'] = group


        try:
            instanced = User.objects.get(pk=pk)
        except:
            instanced = None




        data['date_joined'] = datetime.datetime.now()
        response = {}
        forma = FormCreator()
        forma = forma.form_to_model(modelo=User,excludes = [])
        if  instanced:
            forma.base_fields['password'].required=False
        else:
            forma.base_fields['password'].required=True
        forma.base_fields['email'].required=True
        forma.base_fields['groups'].required=True
        
        data['is_active']=True
        data['is_staff']=True
        
        
        if passs:
            data['password']=make_password(data['password'])
        
        forma = forma(data,instance=instanced)

        if forma.is_valid():
            saved = forma.save()

            response['saved'] = 'ok'
            response['datos'] = {'msg':u'guardao con éxito','liga':'/admin/users/'}
            response['callback'] = 'reg_success_user'

        else:
            response['msg'] = 'Verifique su información'
            response['errors'] = forma.errors


        returns = HttpResponse(simplejson.dumps(response))
        
        return returns

Son = Son.as_view()





class saveUser(View):

    def post(self,request):
        data = request.POST.copy()
        passs = request.POST.get('password',None)
        pk = request.POST.get('gpk',None)
        permisos = request.POST.getlist('perms[]')
        if pk and permisos:
            g = Group.objects.get(pk=pk)
            instanced,failins = Permission.objects.get_or_create(grupo=g)
            instanced.permisos = simplejson.dumps(permisos)
            instanced.save()

            response = {'saved':instanced.pk}
        else:
            response = {'error':'some error ocur'}

        returns = HttpResponse(simplejson.dumps(response))
        
        return returns

saveUser = saveUser.as_view()








class Grupo(View):


    def get(self,request,pk):
        context = {}
        g = Group.objects.get(pk=pk)
        
        try:
            permisos = g.permission_set.all()[0].permslist()
        except:
            permisos = []
        
        self.template = 'admins/grupos.html'
        context['grupo']=g
        context['permisos']=permisos
        context['grupos'] = Group.objects.all().order_by('name')

        response = render(request, self.template, context)
        return response

    def post(self,request):
        data = request.POST.copy()
        passs = request.POST.get('password',None)
        pk = request.POST.get('userpk',None)
        permisos = request.POST.getlist('perms[]')
        if pk and permisos:
            instanced,failins = Permission.objects.get_or_create(usuario_id=pk)
            instanced.permisos = simplejson.dumps(permisos)
            instanced.save()

            response = {'saved':instanced.pk}
        else:
            response = {'error':'some error ocur'}

        returns = HttpResponse(simplejson.dumps(response))
        
        return returns

Grupo = Grupo.as_view()




class addGroup(View):

    def get(self,request):
        data = request.GET.copy()
        name = request.GET.get('name',None)

        if name:
            g,failg = Group.objects.get_or_create(name=name)
            g.save()
            response = {'saved':g.pk}
        else:
            response = {'error':'some error ocur'}

        returns = HttpResponse(simplejson.dumps(response))
        
        return returns

addGroup = addGroup.as_view()


class chGroup(View):

    def get(self,request):
        data = request.GET.copy()
        #name = request.GET.get('name',None)
        pk = data.get('pk',None)
        grupo = data.get('grupo',None)
        if pk and grupo:
            u = User.objects.get(pk=pk)
            u.groups.clear()
            u.groups.add(Group.objects.get(name=grupo))
                        
            response = {'saved':u.pk}
        else:
            response = {'error':'grupo o/y usuario no validos'}

        returns = HttpResponse(simplejson.dumps(response))
        
        return returns

chGroup = chGroup.as_view()



from django import forms

class NameForm(forms.Form):
    subject_sender = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_sender = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    all_users = forms.CharField(widget=forms.CheckboxInput(),required=False)
    texto = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    attached = forms.FileField(required=False)



class senderMail(View):
    template = 'admins/sender.html'
    

    def post(self,request):
        forma = NameForm(request.POST)
        data = request.POST.copy()
        users = data.get('email_sender',None)
        allof = data.get('all_users',None)
        subjt = data.get('subject_sender','Mensaje Normatividad Claro')
        mesgg = data.get('texto',None)
        if forma.is_valid():

            connection = get_connection() # uses SMTP server specified in settings.py
            connection.open()

            if allof:
                uss = User.objects.filter(email__isnull=False)
                allusers = [x.email for x in uss]
                html_content = mesgg #render_to_string('newsletter.html', {'newsletter': n,})               
                text_content = ""                      
                msg = EmailMultiAlternatives(subjt,text_content, "claro@normatividadclaro.com",to=['claro@normatividadclaro.com'],bcc=allusers, connection=connection)                                      
                msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
                msg.send()
                #res = send_mass_mail(allusers, fail_silently = False)

            else:
                mensaje = []
                users = users.split(';')
                #for x in users:
                #    mensaje.append((subjt,mesgg, 'claro@normatividadclaro.com', [x]))

                html_content = mesgg #render_to_string('newsletter.html', {'newsletter': n,})               
                text_content = ""                      
                msg = EmailMultiAlternatives(subjt,text_content, "claro@normatividadclaro.com",to=['claro@normatividadclaro.com'],bcc=users, connection=connection)                                      
                msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
                msg.send()
                #res = send_mass_mail(mensaje, fail_silently = False)
            
            connection.close()

            response = {'saved':'ok','callback':'sendedmail'}
        else:
            response = {'errors':forma.errors,
                        'msg':'Debe llenar los campos'
            }

        return HttpResponse(simplejson.dumps(response))

    def get(self,request):
        context = {}
        forma = NameForm()


        context['forma'] = forma

        response = render(request, self.template, context)
        return response        

senderMail = senderMail.as_view()













