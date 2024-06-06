from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from aceshigh.fields import AceEditorField
from aceshigh.common import MODE_CHOICES, THEME_CHOICES, FONT_SIZE_CHOICES
User = get_user_model()


class EditorProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=14)
    default_theme = models.CharField(max_length=50, choices=THEME_CHOICES, default="github")
    default_mode = models.CharField(max_length=50, choices=MODE_CHOICES, default="html")
    default_editor_css = models.CharField(max_length=200, default="width: 100%;  height: 500px;", null=True, blank=True)
    enable_snippets = models.BooleanField(default=False)


class EditorModeProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mode_profiles")
    mode = models.CharField(max_length=50, choices=MODE_CHOICES)
    font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=14)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default="github")
    editor_css = models.CharField(max_length=200, default="width: 100%;  height: 500px;", null=True, blank=True)


class EditorSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    mode = models.CharField(
        max_length=50, choices=MODE_CHOICES, default="html"
    )
    tags = TaggableManager(blank=True)
    snippet = AceEditorField()
    public = models.BooleanField(default=False)
