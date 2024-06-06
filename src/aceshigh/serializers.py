from rest_framework import serializers
from .models import EditorSnippet


class EditorSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorSnippet
        fields = ["id", "title", "mode", "tags_list", "snippet", "public"]
