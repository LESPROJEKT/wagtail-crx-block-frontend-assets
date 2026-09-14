from collections.abc import Mapping

from wagtail import hooks
from wagtail.blocks.stream_block import StreamValue

from wagtail_crx_block_frontend_assets.blocks import BlockStaticAssetsRegistrationMixin

try:
    from coderedcms.blocks.layout_blocks import BaseLayoutBlock
except ImportError:
    BaseLayoutBlock = None


@hooks.register('before_serve_page')
def collect_block_assets(page, request, serve_args, serve_kwargs):
    static_files = get_blocks_static_assets(getattr(page, "body", None))

    distinct_assets = list({asset.path: asset for asset in static_files}.values())

    request.block_assets = distinct_assets


def _is_layout_block(block):
    return BaseLayoutBlock is not None and issubclass(
        block.block.__class__, BaseLayoutBlock
    )


def _nested_stream_values(value):
    """Yield nested StreamValues from a block value."""
    if isinstance(value, StreamValue):
        yield value
        return

    if isinstance(value, Mapping):
        children = value.values()
    elif isinstance(value, (list, tuple)):
        children = value
    else:
        return

    for child in children:
        yield from _nested_stream_values(child)


def _layout_content_stream(block):
    try:
        content = block.value["content"]
    except (KeyError, TypeError):
        return None

    if content and isinstance(content, StreamValue):
        return content
    return None


def get_blocks_static_assets(body):
    static_files = []

    if not body:
        return static_files

    for block in body:
        if isinstance(block.block, BlockStaticAssetsRegistrationMixin):
            static_files.extend(
                block.block.register_assets(block.value)
            )
            continue

        nested_streams = []
        if _is_layout_block(block):
            content = _layout_content_stream(block)
            if content is not None:
                nested_streams.append(content)

        if not nested_streams:
            nested_streams.extend(_nested_stream_values(block.value))

        for nested in nested_streams:
            static_files.extend(get_blocks_static_assets(nested))

    return static_files
