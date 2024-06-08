from aceshigh.widgets import BaseAceEditorWidget
from django import forms
from django.contrib import admin

from .models import YourModel


class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = "__all__"
        widgets = {
            "content": BaseAceEditorWidget(attrs={"class": "ace-editor"}),
        }


class YourModelAdmin(admin.ModelAdmin):
    form = YourModelForm


admin.site.register(YourModel, YourModelAdmin)
