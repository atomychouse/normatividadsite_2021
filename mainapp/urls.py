# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
   url(r'^$', MViews.Index),
   url(r'^dw/$', (MViews.Download), name='dw'),    
   url(r'^singin/$', MViews.Sin,name='singin'),
   url(r'^home/$', login_required(MViews.Home),name='home'),
   url(r'^singon/$', login_required(MViews.Son),name='singon'),
   url(r'^section/(?P<subsection>[\w-]+)/$', login_required(MViews.Udetail), name='section'),   
   url(r'^section/(?P<section>[\w-]+)/(?P<column>[\w-]+)/(?P<subsection>[\w-]+)$', login_required(MViews.Udetail), name='section'),   
   #url(r'^subsection/(?P<secly>[\w-]+)/(?P<lugy>[\w-]+)/$', login_required(MViews.SUdetail), name='subsection'),   
   url(r'^sections/$', login_required(MViews.Seclist),name='secciones'),
   url(r'^allsections/$', login_required(MViews.AllSeclist),name='allsecciones'),
   url(r'^sender/$', login_required(MViews.Sender),name='sender'),
   url(r'^cropulec/$', login_required(MViews.Crop),name='cropulec'),
   url(r'^campanyas/$', login_required(MViews.Camps),name='campanyas'),
   url(r'^listcampanyas/$', login_required(MViews.listCamps),name='listcampanyas'),

]

