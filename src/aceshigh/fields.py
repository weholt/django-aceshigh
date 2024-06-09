from typing import Any
from django.db import models
from .widgets import AceEditorWidget

class AceEditorField(models.TextField):
    def __init__(self, *args, mode='html', theme='ace/theme/github', **kwargs):
        self.mode = mode
        self.theme = theme
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {**kwargs}
        defaults.update({'widget': AceEditorWidget(attrs={'data-mode': self.mode, 'data-theme': self.theme}, theme=self.theme, mode=self.mode)})
        return super().formfield(**defaults)
