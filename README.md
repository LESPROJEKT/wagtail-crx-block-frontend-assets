# Wagtail CRX block frontend assets rendering

[![PyPI version](https://img.shields.io/pypi/v/wagtail-crx-block-frontend-assets.svg)](https://pypi.org/project/wagtail-crx-block-frontend-assets/) [![Python versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/wagtail-crx-block-frontend-assets/) [![Django tested](https://img.shields.io/badge/django-3.2%20%7C%204.2%20%7C%205.0-blue)](https://www.djangoproject.com/) [![Wagtail tested](https://img.shields.io/badge/wagtail-4.2%20LTS%20%7C%205.2%20LTS%20%7C%206.3%20LTS-blue)](https://wagtail.org/) [![CodeRed CMS tested](https://img.shields.io/badge/coderedcms-2.x%20%7C%203.x%20%7C%204.x%20%7C%205.x-blue)](https://pypi.org/project/coderedcms/) [![License](https://img.shields.io/pypi/l/wagtail-crx-block-frontend-assets.svg)](https://pypi.org/project/wagtail-crx-block-frontend-assets/)

Define and organize frontend assets (like js or css files) for your Wagtail CRX blocks.

## Supported versions

- See the badges above for tested versions.
- "Locked" and "floating" dependency sets are tested.
- Locked sets pin Django + Wagtail + CodeRed via `constraints/*.txt`.
- Floating sets pin Wagtail + CodeRed only, letting Django float within their ranges.
- To support a new version, add a constraint file in `constraints/` and a matching tox/CI entry.

## Getting started

1. Add the app to INSTALLED_APPS:
   ```
   INSTALLED_APPS = [
    ...
    "wagtail_crx_block_frontend_assets",
    ...
    ]
   ```

2. Integrate your blocks with this app.
   ```
    from wagtail.blocks import CharBlock, StructBlock
    from wagtail_crx_block_frontend_assets.blocks import BlockStaticAssetsRegistrationMixin

    class FrontendAssetsBlock(BlockStaticAssetsRegistrationMixin, StructBlock):

        title = CharBlock(
            required=False,
            label="Title",
        )

        def register_assets(self, block_value):
            static_assets = []

            static_assets += [
                self.StaticAsset("path/to/asset.js", target="_blank"),
                self.StaticAsset("path/to/style.css", media="print"),

            ]

            return static_assets
   ```
   Your block class has to inherit from `BlockStaticAssetsRegistrationMixin` and you have to implement `register_assets` function.
   This function returns array of `BlockStaticAssetsRegistrationMixin.StaticAsset` instances.
   You can use `block_value` parameter to conditionally render assets based on current block values.

3. Then you can define place in your templates where you want your block assets to be rendered like this:
    ```
    {% extends "coderedcms/pages/base.html" %}
    {% load block_assets_tags %}

    {% block custom_assets %}
    {{ block.super }}
    {% render_block_assets required_file_extension=".css" %}
    {% endblock custom_assets %}

    {% block custom_scripts %}
    {{ block.super }}
    {% render_block_assets required_file_extension=".js" %}
    {% endblock custom_scripts %}
    ```

## Development

1. Make sure you have Python virtual env installed
    ```
    $ python -m venv .venv
    ```
2. Install this app in editable mode
    ```
    $ pip install -e .
    ```
3. Run tests (single environment)
    ```
    $ pip install -e .[test]
    $ pytest
    ```
4. Run the compatibility matrix
    ```
    $ tox
    ```
5. Migrate testapp DB
    ```
    $ python manage.py migrate
    ```
6. Run the testapp
    ```
    $ python manage.py runserver
    ```
    Or hit F5 if you use Visual Studio Code
