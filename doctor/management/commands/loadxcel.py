# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import simplejson
from datetime import datetime, timedelta
import openpyxl
import os
from django.contrib.auth.models import User,Group
from doctor.models import *
import simplejson
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Describe the Command Here"

    def handle(self, *args,**options):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excelfile = '%s/usuarios.xlsx'%BASE_DIR
        # We exclude a first rows, maybe a header
        ROWS_DESPICABLES = 0
        # Extract al files from model
        wb = openpyxl.load_workbook(excelfile, read_only=True) 
        sheet = wb.active

	


        for r in sheet.iter_rows(row_offset=ROWS_DESPICABLES):
            print r[0].value
            passwor = make_password(r[1].value)

            u,nou = User.objects.get_or_create(username=r[0].value)
            u.is_active = True
            u.is_staff = True
            u.password = passwor
            u.first_name =u'%s'%(r[2].value[:20])
            u.last_name =u'%s'%(' ')
            u.email = r[3].value
            u.groups.add(Group.objects.get(name='basic'))
            u.save()            


