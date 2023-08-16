from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db import models
from django import forms
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.contrib.admin.utils import flatten_fieldsets

class Campo(models.Model):
    tipo = models.CharField(max_length=1, choices=(('C', 'Caracteres'), ('D', 'Decimal'), ('T', 'Texto')))
    nome = models.CharField(max_length=50)
    app = models.CharField(max_length=25)
    tabela = models.CharField(max_length=100)

class MyModel(models.Model):
    descricao = models.CharField(max_length=50)

from django.contrib import admin


class CampoForm(forms.ModelForm):
    on_class = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['on_init'] = forms.CharField(required=False)
        for fieldname in ('foo', 'bar', 'baz',):
            self.fields[fieldname] = forms.CharField()


class MyModelForm(CampoForm):

    class Meta:
        model = MyModel
        fields = '__all__'


class MyModelAdmin(admin.ModelAdmin):
    form = MyModelForm
    fields = ['descricao']
    fieldsets = []

    def get_form(self, request, obj=None, **kwargs):
        kwargs['fields'] = [*flatten_fieldsets(self.fieldsets), *self.fields]
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(MyModelAdmin, self).get_fieldsets(request, obj)

        newfieldsets = list(fieldsets)
        fields = ['foo', 'bar', 'baz']
        newfieldsets.append(['Dynamic Fields', { 'fields': fields }])

        return newfieldsets


admin.site.register(MyModel, MyModelAdmin)
admin.site.register(Campo)
