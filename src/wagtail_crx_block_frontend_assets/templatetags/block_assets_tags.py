from __future__ import annotations

from typing import Iterable

from django import template

from wagtail_crx_block_frontend_assets.wagtail_hooks import get_blocks_static_assets

register = template.Library()


def _collect_assets_from_page(page) -> list:
    """
    Fallback collector used when request.block_assets is not available
    (e.g. in Wagtail preview).
    """
    if not page or not hasattr(page, "body") or page.body is None:
        return []

    static_files = get_blocks_static_assets(page.body)
    return list({asset.path: asset for asset in static_files}.values())


@register.inclusion_tag(
    "wagtail_crx_block_frontend_assets/includes/block_assets.html",
    takes_context=True,
)
def render_block_assets(context, required_file_extension: str | None = None):
    """
    Renders distinct block assets for the current request or page context.
    """
    request = context.get("request")
    assets: Iterable = []

    if request and hasattr(request, "block_assets"):
        assets = request.block_assets or []
    else:
        page = context.get("page") or context.get("self")
        assets = _collect_assets_from_page(page)

    asset_list = list(assets)

    return {
        "assets": asset_list,
        "required_file_extension": required_file_extension,
        "request": request,
    }

