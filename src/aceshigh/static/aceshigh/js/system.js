class Toast {
    constructor() {
        this.toastElement = document.createElement('div');
        this.toastElement.classList.add('toast');
        this.toastElement.style.position = 'fixed';
        this.toastElement.style.top = '50%';
        this.toastElement.style.left = '50%';
        this.toastElement.style.transform = 'translate(-50%, -50%)';
        this.toastElement.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        this.toastElement.style.color = '#fff';
        this.toastElement.style.padding = '20px';
        this.toastElement.style.borderRadius = '8px';
        this.toastElement.style.fontFamily = 'Arial, sans-serif';
        this.toastElement.style.zIndex = '1000';
        this.toastElement.style.display = 'none';
        this.toastElement.style.maxWidth = '300px';
        this.toastElement.style.textAlign = 'center';
        //document.body.appendChild(this.toastElement);
    }

    show(message, duration = 2000) {
        this.toastElement.innerHTML = message;
        this.toastElement.classList.add('show-toast');
        this.toastElement.style.display = 'block';
        setTimeout(() => {
            this.toastElement.style.display = 'none';
            this.toastElement.classList.remove('show-toast');
        }, duration);
    }
}

toast_factory = new Toast();

class Loader {
    static loadCSS(href) {
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

    static loadScript(src, callback) {
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
            script.onerror = function() {
                console.error(`Failed to load script: ${src}`);
            };
            document.head.appendChild(script);
        } else {
            callback();
        }
    }
}

loader = new Loader();

// document.addEventListener("DOMContentLoaded", function() {
//     // Initialize all Ace Editor instances
//     document.querySelectorAll('textarea.ace-editor').forEach((textarea) => {
//         const editor = ace.edit(textarea.id);
//         editor.setTheme("ace/theme/github");
//         editor.session.setMode("ace/mode/javascript");
//         editor.setOptions({
//             enableBasicAutocompletion: true,
//             enableSnippets: true,
//             enableLiveAutocompletion: true,
//             showGutter: true,
//             showLineNumbers: true,
//         });
//         editor.renderer.attachToShadowRoot = true;

//         // Set the initial content
//         editor.setValue(textarea.value, 1);

//         // Update the textarea value on change
//         editor.session.on('change', function() {
//             textarea.value = editor.getValue();
//         });
//     });
// });