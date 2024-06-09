from django.forms import widgets
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe


class InvalidModeError(Exception):
    pass

class InvalidThemeError(Exception):
    pass

class AceEditorWidget(widgets.Textarea):


    def __init__(self, mode="html", theme="ace/theme/github", attrs={}):
        if "/" in mode:
            raise InvalidModeError(f"Invalid mode '{mode}'")   
        if theme.count("/") != 2:
            raise InvalidThemeError(f"Invalid theme '{theme}'. It should have the form of 'ace/theme/<THEME_NAME>'")
        
        self.mode = mode
        self.theme = theme        
        super().__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        text_area_html = super().render(name, value, attrs, renderer)
        editor_id = attrs['id'] if 'id' in attrs else name
        editor_configurations_url = reverse_lazy('aceshigh:editor-configurations')
        editor_profiles_url = reverse_lazy('aceshigh:edit_profile')
        editor_mode_profile_url = reverse_lazy('aceshigh:edit_mode_profile', args=[0])
        process_modal_url = reverse_lazy('aceshigh:process_modal')
        process_text_url = reverse_lazy('aceshigh:process_text')
        fullscreen_icon = static('aceshigh/images/arrows-fullscreen.svg')
        settings_icon = static('aceshigh/images/gear.svg')
        info_icon = static('aceshigh/images/info-circle.svg')
        system_styles = static('aceshigh/css/system.css')

        editor_html = f'''
            <div id="editor_{editor_id}_box" style="margin-top: 20px; position: relative; width: 100%;">
                <div id="editor_{editor_id}" class="ace-editor" data-mode="{self.mode}" data-theme="ace/theme/{self.theme}">
                </div>
            </div>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    const configs = {{
                        editorId: "editor_{editor_id}",
                        editorConfigurationsUrl: "{editor_configurations_url}",
                        editorProfilesUrl: "{editor_profiles_url}",
                        editorModeProfileUrl: "{editor_mode_profile_url}",
                        processModalUrl: "{process_modal_url}",
                        processTextUrl: "{process_text_url}",
                        fullscreenIcon: "{fullscreen_icon}",
                        settingsIcon: "{settings_icon}",
                        infoIcon: "{info_icon}",
                        systemStyles: "{system_styles}"
                    }};
                    initializeEditor(configs);
                }});
            </script>
        '''
        return mark_safe(text_area_html + editor_html)
