# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from campainsapp import views as DViews
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
   url(r'^$', DViews.Index),
   url(r'^upfiles/$', login_required(DViews.upsFiles),name='upfiles'),
   url(r'^runcomand/$', login_required(DViews.runComands),name='runcomand'),
   url(r'^getpendings/$', login_required(DViews.getPendings),name='getpendings'),
   url(r'^edtsingle/$', login_required(DViews.edtSingle),name='edtsingle'),
   url(r'^savesingle/$', login_required(DViews.saveSingle),name='savesingle'),
   url(r'^delsingle/$', login_required(DViews.delSingle),name='delsingle'),
   url(r'^editgroup/$', login_required(DViews.editGroup),name='editgroup'),
   url(r'^savegroup/$', login_required(DViews.saveGroup),name='savegroup'),
   url(r'^rmgroup/$', login_required(DViews.rmGroup),name='rmgroup'),
   url(r'^addtocats/$', login_required(DViews.addTocat),name='addtocats'),
   url(r'^saveall/$', login_required(DViews.saveAll),name='saveall'),
   url(r'^cats/$', login_required(DViews.allCats),name='cats'),
   # FROM SECTIONS PROCCESS
   url(r'^destaca/$', login_required(DViews.Destaca),name='destaca'),

   url(r'^adjuntos/$', login_required(DViews.adjuntaFile),name='adjuntos')



]

