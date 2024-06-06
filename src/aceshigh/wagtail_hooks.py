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
