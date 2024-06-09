from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse

@hooks.register('register_settings_menu_item')
def register_wagtail_editor_profile_menu_item():
    return MenuItem(
        'Editor Profile',
        f"{reverse('aceshigh:edit_profile')}?wagtail=true",
        icon_name='edit',
        order=10000
    )


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/custom.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("aceshigh/css/style.css")
    ) + format_html(
        '<link rel="stylesheet" href="{}">',
        static("aceshigh/css/system.css")
    )


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    return format_html('''
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/ace.js" integrity="sha512-czfWedq9cnMibaqVP2Sw5Aw1PTTabHxMuTOkYkL15cbCYiatPIbxdV0zwhfBZKNODg0zFqmbz8f7rKmd6tfR/Q==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/ext-language_tools.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.9.6/snippets/javascript.js"></script>
        <script>
            let langTools = ace.require("ace/ext/language_tools");
        </script>
        <script src="https://unpkg.com/htmx.org@1.4.1"></script>
        <script src="{}"></script>''',
        static("aceshigh/js/system.js")
    )