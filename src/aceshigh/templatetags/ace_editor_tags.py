import time
from django import template
from django.template.loader import render_to_string
from aceshigh.models import EditorProfile, EditorSnippet

register = template.Library()


@register.simple_tag(takes_context=True)
def ace_editor(context, textarea_id, mode=None, add_scripts="1", theme=None, font_size=None):
    add_scripts = add_scripts and add_scripts.lower() in ["true", "1", "yes"]
    user = context["request"].user
    profile = EditorProfile.objects.filter(user=user).first()
    mode = mode or profile.default_mode if profile else "html"
    snippets_by_mode = {}
    if profile and profile.enable_snippets:
        snippets = EditorSnippet.objects.filter(user=user, mode=mode)
        for snippet in snippets:
            if snippet.mode not in snippets_by_mode:
                snippets_by_mode[snippet.mode] = []
            snippets_by_mode[snippet.mode].append(
                {
                    "title": snippet.title,
                    "content": snippet.snippet,
                }
            )

    css = profile.editor_css if profile else "#editor { width: 100%; height: 500px; }"
    editor_css = profile.editor_css or ""
    enable_snippets = profile.enable_snippets if profile else False
    theme = theme or profile.theme if profile else "github"
    font_size = font_size or profile.font_size if profile else 14
    random_id = str(time.time()).replace(".", "")

    return render_to_string(
        "aceshigh/partials/ace_editor.html",
        {
            "textarea_id": textarea_id,
            "random_id": random_id,
            "css": css,
            "add_scripts": add_scripts,
            "enable_snippets": enable_snippets,
            "theme": theme,
            "mode": mode,
            "font_size": font_size,
            "snippets_by_mode": snippets_by_mode,
            "editor_css": editor_css,
        },
    )
