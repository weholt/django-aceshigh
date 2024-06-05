from django.urls import path
from . import views

app_name = "aceshigh"

urlpatterns = [
    path("", views.edit_profile, name="edit_profile"),
    path("mode_profile/add/", views.add_mode_profile, name="add_mode_profile"),
    path("mode_profile/edit/<int:mode_profile_id>/", views.edit_mode_profile, name="edit_mode_profile"),
    path(
        "mode_profile/delete/<int:mode_profile_id>/", views.delete_mode_profile, name="delete_mode_profile"
    ),
    path("snippet/add/", views.add_snippet, name="add_snippet"),
    path("snippet/edit/<int:snippet_id>/", views.edit_snippet, name="edit_snippet"),
    path(
        "snippet/delete/<int:snippet_id>/", views.delete_snippet, name="delete_snippet"
    ),
    path("snippets/export/", views.export_snippets, name="export_snippets"),
    path("snippets/import/", views.import_snippets, name="import_snippets"),
    path("snippets/public/", views.public_snippets, name="public_snippets"),
    path('editor-configurations/', views.get_editor_configurations, name='editor-configurations'),
]
