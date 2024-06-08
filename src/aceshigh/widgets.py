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
            "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ext-modelist.js",  
            "https://unpkg.com/htmx.org@1.4.1",
            static('aceshigh/js/system.js'),
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
        editor_profiles_url = reverse_lazy('aceshigh:edit_profile')
        editor_mode_profile_url = reverse_lazy('aceshigh:edit_mode_profile', args=[0])
        process_modal = reverse_lazy('aceshigh:process_modal')
        process_text = reverse_lazy('aceshigh:process_text')
        fullscreen_icon = static('aceshigh/images/arrows-fullscreen.svg')
        settings_icon = static('aceshigh/images/gear.svg')
        info_icon = static('aceshigh/images/info-circle.svg')
        system_scripts_url = static('aceshigh/js/system.js')
        system_styles = static('aceshigh/css/system.css')
        snippets_js = "\n".join([f"snippet {s['trigger']}\n\t{s['content']}" for s in self.snippets])
        editor_html = f'''

            <div class="modal fade" id="processModal" tabindex="-1" aria-labelledby="processModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="processModalLabel">Process Selected Text</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" id="modal-body">
                            <!-- Form content will be loaded here via htmx -->
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" id="proceed-button">Proceed</button>
                        </div>
                    </div>
                </div>
            </div>

            <div id="toast" class="toast"></div>
            <div id="editor_box_{editor_id}" style="position: relative; width: 100%;">
                <div id="editor_{editor_id}" class="ace-editor">
                </div>
            </div>
            <script>
                                          
                document.addEventListener("DOMContentLoaded", function() {{
                    fetch('{editor_configurations_url}')
                        .then(response => response.json())
                        .then(configurations => {{
                            
                        
                            function loadCSS(href) {{
                                const existingStylesheets = document.querySelectorAll('link[rel="stylesheet"]');
                                let isLoaded = false;

                                existingStylesheets.forEach(stylesheet => {{
                                    if (stylesheet.href === href) {{
                                        isLoaded = true;
                                    }}
                                }});

                                if (!isLoaded) {{
                                    const link = document.createElement('link');
                                    link.rel = 'stylesheet';
                                    link.href = href;
                                    document.head.appendChild(link);
                                }}
                            }}                         
                            loadCSS('{system_styles}');

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
                                enableBasicAutocompletion: config['enable_basic_autocompletion'] || true,
                                enableLiveAutocompletion: config['enble_live_autocompletion'] || true,
                                showGutter: config['show_gutter'] || false,
                                showLineNumbers: config['show_line_numbers'] || false,
                                //fontFamily: "BPmono",
                            }});

                            //editor.setKeyboardHandler(config['keybinding'] || "ace/keyboard/vim");
                            //editor.setDefaultHandler(config['keybinding'] || "ace/keyboard/vim");
                            //console.log(editor.getKeyboardHandler())

                            if (config['style']) {{
                                editorDiv.style.cssText += config['style'];
                            }}

                            var imageContainer = document.getElementById('editor_box_{editor_id}');

                            var img = document.createElement('img');
                            img.src = '{fullscreen_icon}';
                            img.classList.add('fullscreen-icon');
                            img.style="position: absolute; top: -20px; right: 5px; cursor: pointer;";                            
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

                            var img_editor_profile = document.createElement('img');
                            img_editor_profile.src = '{settings_icon}';
                            img_editor_profile.style="position: absolute; top: -20px; right: 30px; cursor: pointer;";
                            imageContainer.insertBefore(img_editor_profile, imageContainer.firstChild);    
                            img_editor_profile.addEventListener('click', function() {{
                                if (config['mode_id'] === undefined) {{
                                    window.location.href = '{editor_profiles_url}' + '?next=' + window.location.href;
                                }} else {{
                                    window.location.href = '{editor_mode_profile_url}'.replace('0', config['mode_id']) + '?next=' + window.location.href;                                    
                                }}
                            }})                                                    

                            var img_info = document.createElement('img');
                            img_info.src = '{info_icon}';
                            img_info.style="position: absolute; top: -20px; right: 60px; cursor: pointer;";
                            imageContainer.insertBefore(img_info, imageContainer.firstChild);    
                            img_info.addEventListener('click', function() {{
                                showEditorInfoToast(editor);
                            }})                                                    
                                    
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

                            editor.commands.addCommand({{
                                name: 'processSelectedText',
                                bindKey: {{win: 'Ctrl-Alt-1', mac: 'Command-Alt-1'}},
                                exec: function(editor) {{
                                    const selectedText = editor.getSelectedText();
                                    if (selectedText) {{
                                        showProcessModal(selectedText, editor);
                                    }} else {{
                                        toast.show("No text selected", 2000);
                                    }}
                                }}
                            }});

                            function showProcessModal(selectedText, editor) {{
                                const modalBody = document.getElementById('modal-body');
                                const csrfToken = getCookie('csrftoken');
                                htmx.ajax('POST', '{process_modal}', {{
                                    target: '#modal-body',
                                    headers: {{
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': csrfToken
                                    }},
                                    values: {{
                                        selected_text: selectedText,
                                        mode: "{self.mode}"
                                    }}
                                }});

                                const processModal = new bootstrap.Modal(document.getElementById('processModal'));
                                processModal.show();

                                // Set up the proceed button to send the selected text and form data
                                document.getElementById('proceed-button').onclick = function() {{
                                    const formData = new FormData(document.querySelector('#modal-body form'));
                                    const formObject = Object.fromEntries(formData.entries());
                                    formObject.selected_text = selectedText;

                                    fetch('{process_text}', {{
                                        method: 'POST',
                                        headers: {{
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': getCookie('csrftoken') // CSRF token for Django
                                        }},
                                        body: JSON.stringify(formObject)
                                    }})
                                    .then(response => response.json())
                                    .then(data => {{
                                        console.log(data)
                                        const processedText = data.processed_text;
                                        const range = editor.getSelectionRange();
                                        editor.session.replace(range, processedText);
                                        console.log("Text processed successfully", 2000);
                                        processModal.hide();
                                    }})
                                    .catch(error => {{
                                        console.error('Error:', error);
                                        toast.show("Error processing text", 2000);
                                    }});
                                }};
                            }}

                            function getCookie(name) {{
                                let cookieValue = null;
                                if (document.cookie && document.cookie !== '') {{
                                    const cookies = document.cookie.split(';');
                                    for (let i = 0; i < cookies.length; i++) {{
                                        const cookie = cookies[i].trim();
                                        if (cookie.substring(0, name.length + 1) === (name + '=')) {{
                                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                            break;
                                        }}
                                    }}
                                }}
                                return cookieValue;
                            }}                                                        
                            
                            function showEditorInfoToast(editor) {{
                                const toast = document.getElementById('toast');
                                const options = editor.getOptions();
                                const mode = editor.session.getMode().$id;
                                const theme = editor.getTheme();
                                const fontSize = editor.getFontSize();
                                const keybinding = options.keyBinding ? options.keyBinding.$id : 'default';

                                toast.innerHTML = `
                                    <strong>Editor Information:</strong><br>
                                    <table style="width: 100%; color: white; text-align: left;">
                                        <tr>
                                            <td>Mode:</td>
                                            <td>${{ mode }}</td>
                                        </tr>
                                        <tr>
                                            <td>Theme:</td>
                                            <td>${{ theme }}</td>
                                        </tr>
                                        <tr>
                                            <td>Font Size:</td>
                                            <td>${{ fontSize }}</td>
                                        </tr>
                                        <tr>
                                            <td>Keybinding:</td>
                                            <td>${{ keybinding }}</td>
                                        </tr>
                                        <tr>
                                            <td>Autocompletion:</td>
                                            <td>${{ options.enableBasicAutocompletion }}</td>
                                        </tr>
                                        <tr>
                                            <td>Live Autocompletion:</td>
                                            <td>${{ options.enableLiveAutocompletion }}</td>
                                        </tr>
                                        <tr>
                                            <td>Show Gutter:</td>
                                            <td>${{ options.showGutter }}</td>
                                        </tr>
                                        <tr>
                                            <td>Show Line Numbers:</td>
                                            <td>${{ options.showLineNumbers }}</td>
                                        </tr>
                                    </table>
                                `;
                                toast.classList.add('show-toast');

                                setTimeout(() => {{
                                    toast.classList.remove('show-toast');
                                }}, 10000);
                            }}

                        }})
                        .catch(error => console.error('Error fetching configurations:', error));
                }});

            </script>
        '''
        return mark_safe(text_area_html + editor_html)

class AceEditorWidget(BaseAceEditorWidget):
    pass