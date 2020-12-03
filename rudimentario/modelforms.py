# -*- encoding: utf-8 -*-

from django.forms import ModelForm
from django import forms


class FormCreator:

    def __init__(self):
        pass



    def form_to_model(self, modelo, fields=None, widgets=None, excludes=None,fields_required=None):
        meta = type('Meta', (), {
                    "model": modelo, 'fields': fields, 'widgets': widgets, 'exclude': excludes})
        KtemodelfomrKlss = type('modelform', (ModelForm,), {"Meta": meta})
        return KtemodelfomrKlss
