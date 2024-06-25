# from aceshigh.blocks import AceEditorBlock, AceHtmlBlock
from aceshigh.fields import AceEditorField
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page


class HomePage(Page):
    content = AceEditorField(mode="html", null=True, blank=True)
    css_content = AceEditorField(mode="css", null=True, blank=True)
    js_content = AceEditorField(mode="javascript", null=True, blank=True)
    python_content = AceEditorField(mode="python", null=True, blank=True)
    markdown_content = AceEditorField(mode="markdown", null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("content"),
        FieldPanel("css_content"),
        FieldPanel("js_content"),
        FieldPanel("python_content"),
        FieldPanel("markdown_content"),
    ]


# class MyPage(Page):
#     body = StreamField([
#         ('some_html', AceHtmlBlock()),
#     ])

#     content_panels = Page.content_panels + [
#         FieldPanel('body'),
#     ]
