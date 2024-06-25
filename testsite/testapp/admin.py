from aceshigh.widgets import AceEditorWidget
from django import forms
from django.contrib import admin

from .models import YourModel


class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = "__all__"
        # widgets = {
        #    "content": AceEditorWidget(attrs={"class": "ace-editor"}),
        # }


class YourModelAdmin(admin.ModelAdmin):
    # form = YourModelForm
    pass


admin.site.register(YourModel, YourModelAdmin)
