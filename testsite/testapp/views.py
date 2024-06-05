from django import forms
from django.shortcuts import render

from .models import YourModel


class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = "__all__"


class TestForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))


def home(request):
    if request.method == "POST":
        form = YourModelForm(request.POST)
        if form.is_valid():
            print("*" * 80)
            print("*" * 80)
            print("Valid:")
            print(form.cleaned_data)
        else:
            print("*" * 80)
            print("*" * 80)
            print("Errors:")
            print(form.errors)

    template_name = "home.html"
    context = {"form2": YourModelForm()}
    return render(request, template_name, context)
