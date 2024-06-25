from rest_framework import generics

from .models import EditorSnippet
from .serializers import EditorSnippetSerializer


class PublicSnippetList(generics.ListAPIView):
    queryset = EditorSnippet.objects.filter(public=True)
    serializer_class = EditorSnippetSerializer
