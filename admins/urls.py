# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as DViews
from . import userviews as UViews 
from . import sectionviews as SViews
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
   url(r'^$', DViews.Index),

   # FROM SECTIONS PROCCESS

   url(r'^addsec/$', login_required(SViews.addSec),name='addsec'),
   url(r'^addcol/$', login_required(SViews.addCol),name='addcol'),
   url(r'^adtrwname/$', login_required(SViews.eddRowN),name='adtrwname'),
   url(r'^rowreorder/$', login_required(SViews.rowReorder),name='rowreorder'),
   url(r'^rowrm/$', login_required(SViews.rowRemover),name='rowrm'),
   url(r'^rmitem/$', login_required(SViews.rmModel),name='rmitem'),
   url(r'^chimage/$', login_required(SViews.chImage),name='chimage'),
   url(r'^publicar/$', login_required(SViews.secPub),name='publicar'),
   url(r'^downlods/$', login_required(SViews.Downlods),name='downlods'),
   url(r'^chlogo/$', login_required(SViews.chLogo),name='chlogo'),
   url(r'^videocvt/$', login_required(DViews.Videocvt),name='videocvt'),
   url(r'^upvideos/$', login_required(DViews.upVideo),name='upvideos'),

   # end section 

   url(r'^addsection/$', login_required(DViews.addSection),name='addsection'),
   #url(r'^addcolumna/$', login_required(DViews.addColumn),name='addcolumna'),
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
   url(r'^removebf/$', login_required(DViews.Rmbancofile),name='removebf'),
   url(r'^uploadbanco/$', login_required(DViews.UploadB),name='uploadbanco'),
   url(r'^addbancofirst/$', login_required(DViews.UploadB),name='addbancofirst'),


   url(r'^updateblank/$', login_required(DViews.updateBlank),name='updateblank'),

   url(r'^addcat/$', login_required(DViews.addCat),name='addcat'),
   url(r'^rmcat/$', login_required(DViews.rmCat),name='rmcat'),
   url(r'^upcat/$', login_required(DViews.upCat),name='upcat'),

   url(r'^adddwlink/$', login_required(DViews.addDwnlink),name='adddwlink'),

   # USERS URL SECTION 
   url(r'^users/$', login_required(UViews.Son),name='users'),
   url(r'^user/$', login_required(UViews.userForm),name='user'),
   url(r'^saveuser/$', login_required(UViews.saveUser),name='saveuser'),
   url(r'^singon/$', login_required(UViews.Son),name='singon'),
   url(r'^grupo/(?P<pk>[\d-]+)/$', login_required(UViews.Grupo),name='grupo'),
   url(r'^addgroup/$', login_required(UViews.addGroup),name='singon'),
   url(r'^chgroup/$', login_required(UViews.chGroup),name='chgroup'),

   url(r'^sender/$', login_required(UViews.senderMail),name='sender'),


   # PARA LAS CATEGORIAS DE CAMPAINS
   url(r'^catlist/$', login_required(DViews.catList),name='catlist'),
   url(r'^catscampains/$', login_required(DViews.mainCats),name='catscampains'),
   url(r'^addcampaincat/$', login_required(DViews.addCampaincat),name='addcampaincat'),
   url(r'^rmcampaincat/$', login_required(DViews.rmCampaincat),name='rmcampaincat'),


#PARA MODULO EXTERNO
   url(r'^saveexterno/$', login_required(DViews.saveExterno),name='saveexterno'),
   url(r'^getexts/$', login_required(DViews.getExterno),name='getexts'),
   url(r'^rmmoduloexterno/$', login_required(DViews.rmModuloEx),name='rmmoduloexterno'),

   url(r'^rmexterno/$', login_required(DViews.rmEx),name='rmexterno'),


   url(r'^campanyaportada/$', login_required(DViews.CampPortada),name='campanyaportada'),



]

