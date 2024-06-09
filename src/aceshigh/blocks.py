# from django.utils.functional import cached_property
# from django.utils.translation import gettext_lazy as _
# from wagtail import blocks
# from wagtail.admin.panels import FieldPanel
# from aceshigh.common import MODE_CHOICES, THEME_CHOICES, FONT_SIZE_CHOICES
# from aceshigh.widgets import AceEditorWidget
# from django.utils.functional import cached_property
# from aceshigh.fields import AceEditorField


# class AceHtmlBlock(blocks.FieldBlock):
    
#     blocks = blocks.Block()

#     def __init__(self, **kwargs):        
#         super().__init__(blocks=('text', blocks.TextBlock()), **kwargs)

#     def get_template(self, value=None, context=None) -> str | None:
#         block_template = super().get_template(value, context)
#         print("block_template", block_template)
#         return block_template

#     @cached_property
#     def field(self):
#         return AceEditorField()
    
#     class Meta:
#         icon = "code"
#         label = _("Ace HTML Editor")
#         form_template = "aceshigh/blocks/ace_editor_block.html"


# class AceEditorBlock(blocks.StructBlock):
#     mode = blocks.ChoiceBlock(choices=MODE_CHOICES, required=True, default='html')
#     theme = blocks.ChoiceBlock(choices=THEME_CHOICES, required=True, default='github')
#     font_size = blocks.ChoiceBlock(choices=FONT_SIZE_CHOICES, required=True, default=14)
#     editor_css = blocks.TextBlock(required=False)
#     content = blocks.TextBlock(required=True)

#     def __init__(
#         self,
#         mode="ace/mode/django",
#         theme="ace/theme/wagtail",
#         required: bool = True,
#         help_text: str = "",
#         validators=(),
#         **kwargs,
#     ):
#         self.field_options = {
#             "required": required,
#             "help_text": help_text,
#             "validators": validators,
#             "mode": mode,
#             "theme": theme,
#         }

#         super().__init__(**kwargs)

#     class Meta:
#         icon = "code"
#         label = _("Ace Editor")
#         form_template = 'blocks/ace_editor_block.html'

#     def get_form_context(self, value, prefix='', errors=None):
#         context = super().get_form_context(value, prefix=prefix, errors=errors)
#         context['MODE_CHOICES'] = MODE_CHOICES
#         context['THEME_CHOICES'] = THEME_CHOICES
#         context['FONT_SIZE_CHOICES'] = FONT_SIZE_CHOICES
#         context['widget'] = AceEditorWidget()
#         context["id"]    = f"{prefix}-{self.meta.label}"
#         context.update(**self.field_options)
#         return context
    
#     @cached_property
#     def field(self):
#         return AceEditorField(**self.field_options)

#     def get_prep_value(self, value):
#         return value

#     def value_from_form(self, value):
#         return value