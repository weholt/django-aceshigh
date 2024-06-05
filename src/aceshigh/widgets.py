from django.templatetags.static import static
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

class BaseAceEditorWidget(forms.Textarea):
    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js',
            'https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ext-language_tools.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-snippets.min.js',
        )

    def __init__(self, attrs=None, mode='html', theme='github', snippets=None, **kwargs):
        self.mode = mode
        self.theme = theme
        self.snippets = snippets if snippets else []
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        text_area_html = super().render(name, value, attrs, renderer)
        editor_id = attrs['id'] if 'id' in attrs else name
        editor_configurations_url = reverse_lazy('aceshigh:editor-configurations')
        icon = static('aceshigh/images/arrows-fullscreen.svg')
        snippets_js = "\n".join([f"snippet {s['trigger']}\n\t{s['content']}" for s in self.snippets])
        editor_html = f'''
            <div id="editor_box_{editor_id}" style="position: relative; width: 100%;">
                <div id="editor_{editor_id}" class="ace-editor">
                </div>
            </div>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    fetch('{editor_configurations_url}')
                        .then(response => response.json())
                        .then(configurations => {{
                            var editorDiv = document.getElementById("editor_{editor_id}");
                            var textarea = document.getElementById("{editor_id}");
                            textarea.style.position = 'absolute';
                            textarea.style.left = '-9999px';

                            var editor = ace.edit(editorDiv);
                            var mode = "{self.mode}";
                            var config = configurations[mode] || configurations['default'] || {{}};
                            textarea.style.left = '-9999px';
                            editor.getSession().on('change', function(){{
                                textarea.value = (editor.getSession().getValue());
                            }});

                            editor.session.setMode(`ace/mode/${{mode}}`);
                            editor.setTheme(config.theme || 'ace/theme/github');
                            editor.setFontSize(config['font-size'] || 14);
                            editor.setOptions({{
                                enableBasicAutocompletion: true,
                                enableSnippets: true,
                                enableLiveAutocompletion: true
                            }});

                            if (config['style']) {{
                                editorDiv.style.cssText += config['style'];
                            }}

                            var img = document.createElement('img');
                            img.src = '{icon}';
                            img.classList.add('fullscreen-icon');
                            img.style="position: absolute; top: -20px; right: 5px; cursor: pointer;";
                            var imageContainer = document.getElementById('editor_box_{editor_id}');
                            imageContainer.insertBefore(img, imageContainer.firstChild);                                                        
                            img.addEventListener('click', function() {{
                                if (!document.fullscreenElement) {{
                                    editorDiv.requestFullscreen().catch(err => {{
                                        console.error("Error attempting to enable full-screen mode: " + err.message);
                                    }});
                                }} else {{
                                    document.exitFullscreen();
                                }}
                            }});

                            var snippetManager = ace.require('ace/snippets').snippetManager;
                            var snippetText = (config.snippets || []).map(snippet => {{
                                var text = snippet.content.join('\\n\t');
                                return `snippet ${{snippet.trigger}}\n\t${{text}}`;
                            }}).join('\\n');

                            var snippetObject = snippetManager.parseSnippetFile(snippetText);
                            snippetManager.register(snippetObject, mode);

                            editor.session.setValue(textarea.value);
                            textarea.form.addEventListener('submit', function() {{
                                textarea.value = editor.getValue();
                            }});
                        }})
                        .catch(error => console.error('Error fetching configurations:', error));
                }});
            </script>
        '''
        return mark_safe(text_area_html + editor_html)

class AceEditorWidget(BaseAceEditorWidget):
    pass