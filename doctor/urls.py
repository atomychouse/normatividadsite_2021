# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as DViews
from . import userviews as UViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
   url(r'^$', DViews.Index),
   url(r'^addsection/$', login_required(DViews.addSection),name='addsection'),
   url(r'^savior/$', login_required(DViews.SaveModel),name='savior'),
   url(r'^remover/$', login_required(DViews.Delmodel),name='remover'),
   url(r'^ishome/$', login_required(DViews.IsHome),name='ishome'),
   url(r'^config/(?P<pk>[\d-]+)/$', login_required(DViews.Adminsection),name='admon_section'),
   url(r'^section_list/$', login_required(DViews.Seclist),name='section_list'),
   url(r'^addrow/$', login_required(DViews.addRow),name='addrow'),
   url(r'^rmrow/$', login_required(DViews.rmRow),name='rmrow'),   
   url(r'^addmedia/$', login_required(DViews.SaveMedia),name='addmedia'),
   url(r'^savedownload/$', login_required(DViews.SaveDwn),name='savedownload'),
   url(r'^reorder/$', login_required(DViews.reorderVw),name='reorder'),
   url(r'^addfile/$', login_required(DViews.AddFile),name='addfile'),
   url(r'^removefile/$', login_required(DViews.delFile),name='removefile'),
   url(r'^updatesection/$', login_required(DViews.UpdateSec),name='updatesection'),


   url(r'^updateblank/$', login_required(DViews.updateBlank),name='updateblank'),

   url(r'^addcat/$', login_required(DViews.addCat),name='addcat'),

   url(r'^adddwlink/$', login_required(DViews.addDwnlink),name='adddwlink'),

   # USERS URL SECTION 
   url(r'^users/$', login_required(UViews.Son),name='users'),
   url(r'^user/$', login_required(UViews.userForm),name='user'),
   url(r'^saveuser/$', login_required(UViews.saveUser),name='saveuser'),
   url(r'^singon/$', login_required(UViews.Son),name='singon'),


]

