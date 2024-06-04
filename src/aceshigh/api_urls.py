from django.urls import path
from . import api_views

app_name = "api"

urlpatterns = [
    path(
        "snippets/", api_views.PublicSnippetList.as_view(), name="public_snippet_list"
    ),
]
