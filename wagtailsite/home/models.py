from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from aceshigh.blocks import AceEditorBlock
from aceshigh.fields import AceEditorField


class HomePage(Page):
    content = AceEditorField(mode='html', null=True, blank=True)
    css_content = AceEditorField(mode='css', null=True, blank=True)
    js_content = AceEditorField(mode='javascript', null=True, blank=True)
    python_content = AceEditorField(mode='python', null=True, blank=True)
    markdown_content = AceEditorField(mode='markdown', null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        FieldPanel('css_content'),
        FieldPanel('js_content'),
        FieldPanel('python_content'),
        FieldPanel('markdown_content'),
    ]    

class MyPage(Page):
    body = StreamField([
        ('html_editor', AceEditorBlock(mode='html', theme='github', font_size=16)),
        ('css_editor', AceEditorBlock(mode='css', theme='solarized_light', font_size=12)),
        ('js_editor', AceEditorBlock(mode='javascript', theme='monokai', font_size=14)),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]    