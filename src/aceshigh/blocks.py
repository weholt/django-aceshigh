from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from aceshigh.common import MODE_CHOICES, THEME_CHOICES, FONT_SIZE_CHOICES
from django.utils.functional import cached_property
from .widgets import AceEditorWidget

class AceEditorBlock(blocks.StructBlock):
    content = blocks.TextBlock(required=True)
    mode = blocks.ChoiceBlock(choices=MODE_CHOICES, required=True, default='html')
    theme = blocks.ChoiceBlock(choices=THEME_CHOICES, required=True, default='github')
    font_size = blocks.ChoiceBlock(choices=FONT_SIZE_CHOICES, required=True, default=14)
    editor_css = blocks.TextBlock(required=False)

    class Meta:
        icon = 'code'
        #form_template = 'blocks/ace_editor_block.html'

    def get_form_context(self, value, prefix='', errors=None):
        context = super().get_form_context(value, prefix=prefix, errors=errors)
        context['MODE_CHOICES'] = MODE_CHOICES
        context['THEME_CHOICES'] = THEME_CHOICES
        context['FONT_SIZE_CHOICES'] = FONT_SIZE_CHOICES
        return context
    
    @cached_property
    def field(self):
        field = super().field
        field.widget = AceEditorWidget()
        return field

    def get_prep_value(self, value):
        return value

    def value_from_form(self, value):
        return value