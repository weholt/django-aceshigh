from django.db import models
from .widgets import AceEditorWidget

class AceEditorField(models.TextField):
    def __init__(self, *args, mode='html', theme='github', **kwargs):
        self.widget = kwargs.pop('widget', AceEditorWidget)
        self.mode = mode
        self.theme = theme
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget(attrs={'data-mode': self.mode, 'data-theme': self.theme}, mode=self.mode)}
        defaults.update(kwargs)
        return super().formfield(**defaults)
