from django import forms
from .models import EditorProfile, EditorSnippet, EditorModeProfile
from django.core.exceptions import ValidationError



class EditorProfileForm(forms.ModelForm):
    class Meta:
        model = EditorProfile
        fields = ["default_font_size", "default_theme", "default_mode", "default_editor_css", 'keybinding', "enable_snippets", 'enable_basic_autocompletion', 'enable_live_atocompletion', 'show_gutter', 'show_line_numbers']
    

class ModeValidator(object):
    def __init__(self, user):
        self.user = user

    def __call__(self, value):
        if EditorModeProfile.objects.filter(user=self.user, mode=value).exists():
            raise ValidationError(f"Mode '{value}' already exists")
        

class EditorModeProfileForm(forms.ModelForm):
    class Meta:
        model = EditorModeProfile
        fields = ["mode", "font_size", "theme", "editor_css", 'keybinding', "enable_snippets", 'enable_basic_autocompletion', 'enable_live_atocompletion', 'show_gutter', 'show_line_numbers']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def clean(self):
        cleaned_data = super().clean()
        item_count = self.instance.pk and 1 or 0        
        mode = cleaned_data.get("mode")
        if mode:
            if EditorModeProfile.objects.filter(user=self.user, mode=mode).count() > item_count:
                raise ValidationError(f"Mode '{mode}' already exists")
        return cleaned_data


class EditorSnippetForm(forms.ModelForm):
    class Meta:
        model = EditorSnippet
        fields = ["title", "mode", "tags", "snippet", "public"]
