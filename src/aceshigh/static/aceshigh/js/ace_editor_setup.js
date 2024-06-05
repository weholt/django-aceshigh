// filename: ace_editor_setup.js

document.addEventListener("DOMContentLoaded", function() {
    fetch('/editor-configurations/')
        .then(response => response.json())
        .then(configurations => initializeEditors('.ace-editor', configurations))
        .catch(error => console.error('Error fetching configurations:', error));

    function initializeEditors(querySelector, editorConfigurations) {
        const editors = document.querySelectorAll(querySelector);

        editors.forEach(editorElement => {
            const editor = ace.edit(editorElement);
            const mode = editorElement.getAttribute('data-mode');
            const config = editorConfigurations[mode] || {};

            editor.session.setMode(`ace/mode/${mode}`);
            editor.setTheme(config.theme || 'ace/theme/github');
            editor.setFontSize(config['font-size'] || 14);
            editor.setOptions({
                enableBasicAutocompletion: true,
                enableSnippets: true,
                enableLiveAutocompletion: true
            });

            if (config['style']) {
                editorElement.style.cssText += config['style'];
            }

            const fullscreenIcon = document.createElement('span');
            fullscreenIcon.innerHTML = '🔍';
            fullscreenIcon.style.position = 'absolute';
            fullscreenIcon.style.top = '5px';
            fullscreenIcon.style.right = '5px';
            fullscreenIcon.style.cursor = 'pointer';
            fullscreenIcon.addEventListener('click', () => toggleFullscreen(editorElement));
            editorElement.style.position = 'relative';
            editorElement.appendChild(fullscreenIcon);

            const snippetManager = ace.require('ace/snippets').snippetManager;
            const snippetText = (config.snippets || []).map(snippet => {
                return `snippet ${snippet.trigger}\n\t${snippet.content}`;
            }).join('\n');

            const snippetObject = snippetManager.parseSnippetFile(snippetText);
            snippetManager.register(snippetObject, mode);

            function toggleFullscreen(editorElement) {
                if (!document.fullscreenElement) {
                    editorElement.requestFullscreen().catch(err => {
                        console.error(`Error attempting to enable full-screen mode: ${err.message}`);
                    });
                } else {
                    document.exitFullscreen();
                }
            }
        });
    }

    ensureAceModulesLoaded(() => initializeEditors('.ace-editor'));

    function ensureAceModulesLoaded(callback) {
        const requiredModules = [
            'ace/ext/language_tools',
            'ace/snippets'
        ];

        let loadedModules = 0;

        function moduleLoaded() {
            loadedModules += 1;
            if (loadedModules === requiredModules.length) {
                callback();
            }
        }

        requiredModules.forEach(module => {
            if (!ace.require(module)) {
                const moduleName = module.split('/').pop();
                const scriptName = module === 'ace/snippets' ? 'mode-snippets' : `ext-${moduleName}`;
                loadScript(`https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/${scriptName}.min.js`, moduleLoaded);
            } else {
                moduleLoaded();
            }
        });
    }

    function loadScript(src, callback) {
        const script = document.createElement('script');
        script.src = src;
        script.onload = callback;
        script.onerror = function() {
            console.error(`Failed to load script: ${src}`);
        };
        document.head.appendChild(script);
    }
});
# endof
