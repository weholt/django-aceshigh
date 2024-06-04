# AcesHigh

AcesHigh is a Django application designed to integrate the ACE editor into Django forms seamlessly.

## Features
- Customizable ACE editor settings
- Support for multiple ACE editor themes and modes
- Snippet management with tagging support
- Fullscreen editor toggle
- Snippet search and tag cloud visualization
- Public snippet sharing with an API

## Requirements
- Python 3.12+
- Django 5.0+
- django-crispy-forms
- django-crispy-bootstrap5
- django-taggit
- djangorestframework
- drf-yasg

## Installation
1. Install the package:
    ```bash
    pip install aceshigh
    ```

2. Add `aceshigh` and its dependencies to your `INSTALLED_APPS` in `settings.py`:
    ```python
    INSTALLED_APPS = [
        ...
        'crispy_forms',
        'crispy_bootstrap5',
        'taggit',
        'rest_framework',
        'drf_yasg',
        'aceshigh',
    ]

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"
    ```

3. Include the AcesHigh URLs in your `urls.py`:
    ```python
    from django.urls import include, path
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions

    schema_view = get_schema_view(
        openapi.Info(
            title="AcesHigh API",
            default_version='v1',
            description="API for accessing public snippets",
            contact=openapi.Contact(email="thomas@weholt.org"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = [
        ...
        path('aceshigh/', include('aceshigh.urls')),
        path('api/', include('aceshigh.api_urls')),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
    ```

## Usage
- To add the ACE editor to any form, use the `{% ace_editor %}` template tag in your templates.

## License
This project is licensed under the GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later).

## Credits
- [ACE Editor](https://github.com/ajaxorg/ace)