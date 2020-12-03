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
            permisos = instanced.permission_set.all()
            if permisos:
                permisos = permisos[0].permslist()
        else:
            instanced = None
            permisos = []


        widgets = {
            'password':forms.PasswordInput(),
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
            response['datos'] = {'msg':u'guardao con éxito','liga':'/admins/users/'}
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

saveUser = saveUser.as_view()



















