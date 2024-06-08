import time
from django import template
from django.template.loader import render_to_string
from django.templatetags.static import static
from aceshigh.models import EditorProfile, EditorSnippet
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def aceshigh_imports():
    return mark_safe(f"""
    <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/journal/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" crossorigin="anonymous">
    <link href="{static('aceshigh/css/system.css')}">
    """)

@register.simple_tag
def aceshigh_scripts():
    return mark_safe(f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ext-language_tools.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ext-modelist.js"></script>
    <script src="https://unpkg.com/htmx.org@1.4.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.min.js" integrity="sha512-ykZ1QQr0Jy/4ZkvKuqWn4iF3lqPZyij9iRv6sGqLRdTPkY69YX6+7wvVGmsdBbiIfN/8OdsI7HABjvEok6ZopQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js" crossorigin="anonymous"></script>
    <script src="{static('aceshigh/js/system.js')}"></script>""")


@register.simple_tag(takes_context=True)
def ace_editor_(context, textarea_id, mode=None, add_scripts="1", theme=None, font_size=None):
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
        "aceshigh/partials/ace_editor_init.html",
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
