
let msg = null;

class ToastMessage {
    constructor() {
        this.toastElement = document.createElement('div');
        this.toastElement.classList.add('toast-message');
        this.toastElement.style.position = 'fixed';
        this.toastElement.style.top = '20px';
        this.toastElement.style.right = '10px';
        this.toastElement.style.margin = '10px 0 0 0';
        this.toastElement.style.backgroundColor = "#00638e";
        this.toastElement.style.color = "white";
        this.toastElement.style.padding = '20px';
        this.toastElement.style.borderRadius = '8px';
        this.toastElement.style.fontFamily = 'Arial, sans-serif';
        this.toastElement.style.zIndex = '99999';
        this.toastElement.style.display = 'none';
        this.toastElement.style.maxWidth = '300px';
        this.toastElement.style.minWidth = '200px';
        this.toastElement.style.textAlign = 'center';
        this.toastElement.style.alignItems = 'center';  // Center items vertically
        this.toastElement.style.justifyContent = 'center';  // Center items horizontally
        document.body.appendChild(this.toastElement);
    }

    show(message, duration = 2000) {
        console.log("Toast message: " + message)
        this.toastElement.innerHTML = `
            <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 8px; width: 20px; height: 20px;">
                <path fill-rule="evenodd" d="M12 2a10 10 0 100 20 10 10 0 000-20zM11 7a1 1 0 012 0v5a1 1 0 11-2 0V7zm0 7a1 1 0 112 0 1 1 0 01-2 0z" clip-rule="evenodd" />
            </svg>
            ${message}`;
        this.toastElement.style.display = 'flex';
        setTimeout(() => {
            this.toastElement.style.display = 'none';
        }, duration);
    }
}
document.addEventListener("DOMContentLoaded", function() {
    msg = new ToastMessage();
});

function loadCSS(href) {
    const existingStylesheets = document.querySelectorAll('link[rel="stylesheet"]');
    let isLoaded = false;

    existingStylesheets.forEach(stylesheet => {
        if (stylesheet.href === href) {
            isLoaded = true;
        }
    });

    if (!isLoaded) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        document.head.appendChild(link);
    }
}

function loadScript(src, callback) {
    const existingScripts = document.querySelectorAll('script[src]');
    let isLoaded = false;

    existingScripts.forEach(script => {
        if (script.src === src) {
            isLoaded = true;
        }
    });

    if (!isLoaded) {
        const script = document.createElement('script');
        script.src = src;
        script.onload = callback;
        script.onerror = function () {
            console.error(`Failed to load script: ${src}`);
        };
        document.head.appendChild(script);
    } else {
        callback();
    }
}

function addModalMarkup() {
    if (!document.getElementById('processModal')) {
        const bootstrapModalMarkup = `
            <div class="modal" id="processModal" tabindex="-1" aria-labelledby="processModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="processModalLabel">Process Selected Text</h5>
                            <button type="button" class="btn-close" onclick="hideModal('processModal')" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" id="modal-body">
                            <!-- Form content will be loaded here via htmx -->
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" onclick="hideModal('processModal')">Cancel</button>
                            <button type="button" class="btn btn-primary" id="proceed-button">Proceed</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const tailwindModalMarkup = `
            <div id="processModal" tabindex="-1" aria-hidden="true" class="modal tailwind-modal hidden overflow-y-auto overflow-x-hidden fixed justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
                <div class="relative p-4 w-full max-w-2xl max-h-full">
                    <div class="relative bg-white rounded-lg shadow-lg dark:bg-gray-700">
                        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                            <h2 class="text-xl font-semibold text-gray-900 dark:text-white" id="default-modal-label">
                                Process Selected Text
                            </h2>
                        </div>
                        <div class="p-4 md:p-5 space-y-4" id="modal-body">
                            <!-- Form content will be loaded here via htmx -->
                        </div>
                        <div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
                            <button onclick="hideModal('processModal')" data-modal-hide="default-modal" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Cancel</button>
                            <button id="proceed-button" data-modal-hide="default-modal" type="button" class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">Proceed</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const customModalMarkup = `
            <div id="processModal" class="custom-modal" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); z-index:9999; background:white; padding:20px; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
                <div class="custom-modal-header" style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #ddd; padding-bottom:10px;">
                    <h5 style="margin:0;">Process Selected Text</h5>
                    <button onclick="hideModal('processModal')" style="background:none; border:none; font-size:20px; cursor:pointer;">&times;</button>
                </div>
                <div class="custom-modal-body" id="modal-body" style="padding:20px 0;">
                    <!-- Form content will be loaded here via htmx -->
                </div>
                <div class="custom-modal-footer" style="display:flex; justify-content:flex-end; border-top:1px solid #ddd; padding-top:10px;">
                    <button onclick="hideModal('processModal')" style="background:#ddd; border:none; padding:10px 20px; margin-right:10px; cursor:pointer;">Cancel</button>
                    <button id="proceed-button" style="background:#00638e; color:white; border:none; padding:10px 20px; cursor:pointer;">Proceed</button>
                </div>
            </div>
        `;

        const modalContainer = document.createElement('div');
        if (typeof bootstrap !== 'undefined') {
            modalContainer.innerHTML = bootstrapModalMarkup;
        } else if (typeof tailwind !== 'undefined') {
            modalContainer.innerHTML = tailwindModalMarkup;
        } else {
            modalContainer.innerHTML = customModalMarkup;
        }
        document.body.appendChild(modalContainer.firstElementChild);
    }
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        if (typeof bootstrap !== 'undefined' && modal.classList.contains('modal')) {
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        } else if (modal.classList.contains('tailwind-modal')) {
            modal.classList.add('flex');
            modal.classList.remove('hidden');
        } else {
            modal.style.display = 'block';
        }
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        if (typeof bootstrap !== 'undefined' && modal.classList.contains('modal')) {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            bootstrapModal.hide();
        } else if (modal.classList.contains('tailwind-modal')) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        } else {
            modal.style.display = 'none';
        }
    }
}


function showModal(modalId) {
    const modal = document.getElementById(modalId);
    console.log("looking for modal", modalId, modal);
    if (modal) {
        if (typeof bootstrap !== 'undefined' && modal.classList.contains('modal')) {
            console.log("Showing bootstrap modal");
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        } else if (modal.classList.contains('tailwind-modal')) {
            console.log("Showing Tailwind modal");
            modal.style.display = 'flex';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.remove('hidden');
        } else {
            console.log("Showing regular modal");
            modal.style.display = 'block';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.add('show');
        }

        document.body.classList.add('modal-open');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        if (typeof bootstrap !== 'undefined' && modal.classList.contains('modal')) {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            bootstrapModal.hide();
        } else if (modal.classList.contains('tailwind-modal')) {
            modal.classList.add('hidden');
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
            modal.classList.remove('flex');
        } else {
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
            modal.classList.remove('show');
        }

        document.body.classList.remove('modal-open');
    }
}

function showEditorInfoToast(editor, toast_element) {
    const options = editor.getOptions();
    const mode = editor.session.getMode().$id;
    const theme = editor.getTheme();
    const fontSize = editor.getFontSize();
    const keybinding = options.keyBinding ? options.keyBinding.$id : 'default';

    innerHTML = `
            <table class="editor-info" style="width: 100%; text-align: left;">
                <tr>
                    <td>Mode:</td>
                    <td>${mode}</td>
                </tr>
                <tr>
                    <td>Theme:</td>
                    <td>${theme}</td>
                </tr>
                <tr>
                    <td>Font Size:</td>
                    <td>${fontSize}</td>
                </tr>
                <tr>
                    <td>Keybinding:</td>
                    <td>${keybinding}</td>
                </tr>
                <tr>
                    <td>Autocompletion:</td>
                    <td>${options.enableBasicAutocompletion}</td>
                </tr>
                <tr>
                    <td>Live Autocompletion:</td>
                    <td>${options.enableLiveAutocompletion}</td>
                </tr>
                <tr>
                    <td>Show Gutter:</td>
                    <td>${options.showGutter}</td>
                </tr>
                <tr>
                    <td>Show Line Numbers:</td>
                    <td>${options.showLineNumbers}</td>
                </tr>
            </table>
        `;
    msg.show(innerHTML, 5000);
}


function initializeEditor(configs) {
    fetch(configs.editorConfigurationsUrl)
        .then(response => response.json())
        .then(configurations => {

            const editorDiv = document.getElementById(configs.editorId);
            console.log('editorDiv', editorDiv, configs.editorId);
            const editorId = editorDiv.id;
            const textarea = document.getElementById(editorId.replace('editor_', ''));
            textarea.style.position = 'absolute';
            textarea.style.left = '-9999px';

            const editor = ace.edit(editorDiv);
            const mode = editorDiv.getAttribute('data-mode');
            const config = configurations[mode] || configurations['default'] || {};
            textarea.style.left = '-9999px';
            editor.getSession().on('change', function () {
                textarea.value = (editor.getSession().getValue());
            });

            editor.session.setMode(`ace/mode/${mode}`);
            editor.setTheme(config.theme || 'ace/theme/github');
            editor.setFontSize(config['font-size'] || 14);
            editor.setOptions({
                enableBasicAutocompletion: config['enable_basic_autocompletion'] || true,
                enableLiveAutocompletion: config['enable_live_autocompletion'] || true,
                showGutter: config['show_gutter'] || false,
                showLineNumbers: config['show_line_numbers'] || false,
            });

            if (config['style']) {
                editorDiv.style.cssText += config['style'];
            }
            
            const imageContainer = document.getElementById(editorId + '_box');
            const img = document.createElement('img');
            img.src = configs.fullscreenIcon;
            img.classList.add('fullscreen-icon');
            img.style = "position: absolute; top: -20px; right: 5px; cursor: pointer;";
            imageContainer.insertBefore(img, imageContainer.firstChild);
            img.addEventListener('click', function () {
                if (!document.fullscreenElement) {
                    editorDiv.requestFullscreen().catch(err => {
                        console.error("Error attempting to enable full-screen mode: " + err.message);
                    });
                } else {
                    document.exitFullscreen();
                }
            });

            const imgEditorProfile = document.createElement('img');
            imgEditorProfile.src = configs.settingsIcon;
            imgEditorProfile.style = "position: absolute; top: -20px; right: 30px; cursor: pointer;";
            imageContainer.insertBefore(imgEditorProfile, imageContainer.firstChild);
            imgEditorProfile.addEventListener('click', function () {
                if (config['mode_id'] === undefined) {
                    window.location.href = configs.editorProfilesUrl + '?next=' + window.location.href;
                } else {
                    window.location.href = configs.editorModeProfileUrl.replace('0', config['mode_id']) + '?next=' + window.location.href;
                }
            });

            const imgInfo = document.createElement('img');
            imgInfo.src = configs.infoIcon;
            imgInfo.style = "position: absolute; top: -20px; right: 60px; cursor: pointer;";
            imageContainer.insertBefore(imgInfo, imageContainer.firstChild);
            imgInfo.addEventListener('click', function () {
                showEditorInfoToast(editor, configs.editorId);
            });

            const snippetManager = ace.require('ace/snippets').snippetManager;
            const snippetText = (config.snippets || []).map(snippet => {
                const text = snippet.content.join('\n\t');
                return `snippet ${snippet.trigger}\n\t${text}`;
            }).join('\n');

            const snippetObject = snippetManager.parseSnippetFile(snippetText);
            snippetManager.register(snippetObject, mode);

            editor.session.setValue(textarea.value);
            textarea.form.addEventListener('submit', function () {
                textarea.value = editor.getValue();
            });

            editor.commands.addCommand({
                name: 'processSelectedText',
                bindKey: { win: 'Ctrl-Alt-1', mac: 'Command-Alt-1' },
                exec: function (editor) {
                    const selectedText = editor.getSelectedText();
                    if (selectedText) {
                        showProcessModal(selectedText, editor, configs);
                    } else {
                        msg.show("No text selected", 2000);
                    }
                }
            });

            function showProcessModal(selectedText, editor, configs) {
                const csrfToken = getCookie('csrftoken');
                htmx.ajax('POST', configs.processModalUrl, {
                    target: '#modal-body',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    values: {
                        selected_text: selectedText,
                        mode: mode
                    }
                });

                showModal('processModal');

                // Set up the proceed button to send the selected text and form data
                document.getElementById('proceed-button').onclick = function () {
                    const formData = new FormData(document.querySelector('#modal-body form'));
                    const formObject = Object.fromEntries(formData.entries());
                    formObject.selected_text = selectedText;

                    fetch(configs.processTextUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') // CSRF token for Django
                        },
                        body: JSON.stringify(formObject)
                    })
                        .then(response => response.json())
                        .then(data => {
                            const processedText = data.processed_text;
                            const range = editor.getSelectionRange();
                            editor.session.replace(range, processedText);
                            msg.show("Text processed successfully", 2000);
                            hideModal('processModal');
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            msg.show("Error processing text", 2000);
                        });
                };                    
            }

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
        })
        .catch(error => console.error('Error fetching configurations:', error));
}

document.addEventListener("DOMContentLoaded", function() {{
    addModalMarkup();
}});

