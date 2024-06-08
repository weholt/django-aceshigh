from typing import Self
from django.http import HttpRequest
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from .models import EditorProfile, EditorSnippet, EditorModeProfile
from .forms import EditorProfileForm, EditorSnippetForm, EditorModeProfileForm
import json

from .protocols import get_processor_choices, get_processors_classes, get_processor_class


@login_required
def edit_profile(request):
    profile, created = EditorProfile.objects.get_or_create(user=request.user)
    snippets = EditorSnippet.objects.filter(user=request.user)
    mode_profiles = EditorModeProfile.objects.filter(user=request.user)
    search_query = request.GET.get("q")
    if search_query:
        snippets = (
            snippets.filter(title__icontains=search_query)
            | snippets.filter(snippet__icontains=search_query)
            | snippets.filter(tags__name__icontains=search_query)
        )
        snippets = snippets.distinct()
    tags = EditorSnippet.tags.most_common()
    tag_cloud = {tag.name: tag.num_times for tag in tags}
    if request.method == "POST":
        form = EditorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if next := request.POST.get('next'):
                return redirect(next)
            return redirect("aceshigh:edit_profile")
    else:
        form = EditorProfileForm(instance=profile)

    wagtail_source = False #request.GET.get('wagtail', request.POST.get('wagtail'), False)
    template = wagtail_source and 'wagtailadmin/wagtail_editor_profile.html' or "aceshigh/edit_profile.html"
    return render(
        request,
        template,
        {
            "form": form,
            "snippets": snippets,
            "search_query": search_query,
            "tag_cloud": tag_cloud,
            "mode_profiles": mode_profiles,
            "next": request.GET.get("next"),
        },
    )

@login_required
def add_mode_profile(request):
    form = EditorModeProfileForm()
    if request.method == "POST":
        form = EditorModeProfileForm(data=request.POST, user=request.user)
        if form.is_valid():
            mode_profile = form.save(commit=False)
            mode_profile.user = request.user
            mode_profile.save()
            if next := request.POST.get('next'):
                return redirect(next)
            return redirect("aceshigh:edit_profile")
        
    return render(request, "aceshigh/add_mode_profile.html", {"form": form})

@login_required
def edit_mode_profile(request, mode_profile_id):
    mode_profile = get_object_or_404(EditorModeProfile, pk=mode_profile_id, user=request.user)
    if request.method == "POST":
        form = EditorModeProfileForm(data=request.POST, user=request.user, instance=mode_profile)
        if form.is_valid():
            form.save()
            if next := request.POST.get('next'):
                return redirect(next)
            return redirect("aceshigh:edit_profile")
    else:
        form = EditorModeProfileForm(instance=mode_profile)
    return render(request, "aceshigh/edit_mode_profile.html", {"form": form, 'next': request.GET.get('next')})

@login_required
def delete_mode_profile(request, mode_profile_id):
    mode_profile = get_object_or_404(EditorModeProfile, pk=mode_profile_id, user=request.user)
    if request.method == "POST":
        mode_profile.delete()
        return redirect("aceshigh:edit_profile")
    return render(request, "aceshigh/confirm_delete_mode_profile.html", {"mode_profile": mode_profile})


@login_required
def add_snippet(request):
    if request.method == "POST":
        form = EditorSnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            if next := request.POST.get('next'):
                return redirect(next)
            return redirect("aceshigh:edit_profile")
    else:
        form = EditorSnippetForm()
    return render(request, "aceshigh/add_snippet.html", {"form": form})


@login_required
def edit_snippet(request, snippet_id):
    snippet = get_object_or_404(EditorSnippet, pk=snippet_id, user=request.user)
    if request.method == "POST":
        form = EditorSnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            if next := request.POST.get('next', None):
                return redirect(next)
            return redirect("aceshigh:edit_profile")
    else:
        form = EditorSnippetForm(instance=snippet)
    return render(request, "aceshigh/edit_snippet.html", {"form": form, "next": request.GET.get("next")})


@login_required
def delete_snippet(request, snippet_id):
    snippet = get_object_or_404(EditorSnippet, pk=snippet_id, user=request.user)
    if request.method == "POST":
        snippet.delete()
        return redirect("aceshigh:edit_profile")
    return render(request, "aceshigh/confirm_delete_snippet.html", {"snippet": snippet})


def public_snippets(request):
    snippets = EditorSnippet.objects.filter(public=True)
    search_query = request.GET.get("q")
    if search_query:
        snippets = (
            snippets.filter(title__icontains=search_query)
            | snippets.filter(snippet__icontains=search_query)
            | snippets.filter(tags__name__icontains=search_query)
        )
        snippets = snippets.distinct()
    tags = EditorSnippet.tags.most_common()
    tag_cloud = {tag.name: tag.num_times for tag in tags}
    return render(
        request,
        "aceshigh/public_snippets.html",
        {"snippets": snippets, "search_query": search_query, "tag_cloud": tag_cloud},
    )


@login_required
def export_snippets(request):
    snippets = EditorSnippet.objects.filter(user=request.user)
    snippets_list = [
        {
            "title": snippet.title,
            "mode": snippet.mode,
            "tags": list(snippet.tags.names()),
            "snippet": snippet.snippet,
        }
        for snippet in snippets
    ]
    response = HttpResponse(json.dumps(snippets_list), content_type="application/json")
    response["Content-Disposition"] = "attachment; filename=snippets.json"
    return response


@login_required
def import_snippets(request):
    if request.method == "POST" and request.FILES.get("file"):
        snippets_file = request.FILES["file"]
        snippets_data = json.load(snippets_file)
        for snippet_data in snippets_data:
            snippet = EditorSnippet(
                user=request.user,
                title=snippet_data["title"],
                mode=snippet_data["mode"],
                snippet=snippet_data["snippet"],
                public=snippet_data.get("public", False),
            )
            snippet.save()
            snippet.tags.add(*snippet_data["tags"])
        return redirect("aceshigh:edit_profile")
    return render(request, "aceshigh/import_snippets.html")


@login_required
def get_editor_configurations(request):
    default_profile = EditorProfile.objects.filter(user=request.user).first()
    if not default_profile:
        return {}
    
    snippets = default_profile.enable_snippets and EditorSnippet.objects.filter(user=request.user) or []
    editor_configurations = {
        'default': {
            'theme': f"ace/theme/{default_profile.default_theme}", 
            'font-size': default_profile.default_font_size,
            'keybinding': default_profile.keybinding, 
            'enable_basic_autocompletion': default_profile.enable_basic_autocompletion,
            'enable_live_atocompletion': default_profile.enable_live_atocompletion,
            'show_gutter': default_profile.show_gutter, 
            'show_line_numbers': default_profile.show_line_numbers,
            'snippets': [
                {
                    'trigger': snippet.title,
                    'content': snippet.snippet.split("\n")
                }
                for snippet in snippets
            ],
            'style': default_profile.default_editor_css
        }
    }

    mode_profiles = EditorModeProfile.objects.filter(user=request.user)
    for mode_profile in mode_profiles:
        editor_configurations[mode_profile.mode] = {
            'mode_id': mode_profile.id,
            'theme': f"ace/theme/{mode_profile.theme}",
            'font-size': mode_profile.font_size,
            'keybinding': mode_profile.keybinding, 
            'enable_basic_autocompletion': mode_profile.enable_basic_autocompletion,
            'enable_live_atocompletion': mode_profile.enable_live_atocompletion,
            'show_gutter': mode_profile.show_gutter, 
            'show_line_numbers': mode_profile.show_line_numbers,
            'snippets': [
                {
                    'trigger': snippet.title,
                    'content': snippet.snippet.split("\n")
                }
                for snippet in snippets
                if snippet.mode == mode_profile.mode
            ],
            'style': mode_profile.editor_css
        }

    #import pprint
    #pprint.pprint(editor_configurations)
    return JsonResponse(editor_configurations)

@csrf_exempt
@login_required
def process_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = processed_text = data.pop('selected_text', '')
        option = data.pop('dropdown', None)
        mode = request.GET.get('mode', None)
        if processor_klass := get_processor_class(request, option):
            processor = processor_klass(request)  # type: ignore noqa
            extra_data = {}
            if form_klass := processor.get_form_class(mode=mode):
                form = form_klass(data)
                if form.is_valid():
                    extra_data = form.cleaned_data        
            processed_text = processor.process(text, mode, extra_data)
            return JsonResponse({'processed_text': processed_text})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def process_modal(request):
    selected_text = request.POST.get('selected_text', '')
    mode = request.POST.get('mode', 'html')
    return render(request, 'aceshigh/partials/process_modal.html', {'mode': mode,'selected_text': selected_text, 'dropdown_options': get_processor_choices(request)})

@csrf_exempt
@login_required
def fetch_form(request):
    option = request.GET.get('dropdown', None)
    mode = request.GET.get('mode', None)
    form = None
    if processor_klass := get_processor_class(request, option):
        processor = processor_klass(request)  # type: ignore noqa
        if form_klass := processor.get_form_class(mode=mode):
            form = form_klass and form_klass()
    return render(request, 'aceshigh/partials/fetch_form.html', {'form': form, 'mode': mode})