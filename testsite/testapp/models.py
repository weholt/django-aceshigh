from aceshigh.fields import AceEditorField
from django.db import models


class YourModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    content = AceEditorField()
    code = AceEditorField(theme="ace/theme/dracula", mode="python")
