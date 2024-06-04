from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import EditorSnippet
from .serializers import EditorSnippetSerializer


class PublicSnippetList(generics.ListAPIView):
    queryset = EditorSnippet.objects.filter(public=True)
    serializer_class = EditorSnippetSerializer
