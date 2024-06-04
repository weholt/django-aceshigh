from django import forms
from django.shortcuts import render


class TestForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))

def home(request):
    if request.method == "POST":
        form = TestForm(request.POST)   
        if form.is_valid():
            print(form.cleaned_data)
        
    template_name = "home.html"
    context = {"form": TestForm()}
    return render(request, template_name, context)
    