from types import SimpleNamespace

from django.template import Context, Template
from django.test import RequestFactory
from wagtail.blocks import CharBlock, StreamBlock, StructBlock

from wagtail_crx_block_frontend_assets.blocks import BlockStaticAssetsRegistrationMixin
from wagtail_crx_block_frontend_assets.wagtail_hooks import (
    collect_block_assets,
    get_blocks_static_assets,
)


class AssetsBlock(BlockStaticAssetsRegistrationMixin, StructBlock):
    title = CharBlock(required=False)

    def register_assets(self, block_value):
        return [
            self.StaticAsset("test/app.js"),
            self.StaticAsset("test/app.css", media="print"),
        ]


class AssetsStreamBlock(StreamBlock):
    assets = AssetsBlock()


def build_stream_value():
    block = AssetsStreamBlock()
    return block.to_python([{"type": "assets", "value": {"title": "Hello"}}])


def test_get_blocks_static_assets_collects_from_mixin():
    assets = get_blocks_static_assets(build_stream_value())
    assert [asset.path for asset in assets] == ["test/app.js", "test/app.css"]


def test_collect_block_assets_attaches_to_request():
    page = SimpleNamespace(body=build_stream_value())
    request = RequestFactory().get("/")

    collect_block_assets(page, request, (), {})

    assert hasattr(request, "block_assets")
    assert {asset.path for asset in request.block_assets} == {
        "test/app.js",
        "test/app.css",
    }


def test_render_block_assets_template_tag_renders_required_extension():
    page = SimpleNamespace(body=build_stream_value())
    template = Template(
        "{% load block_assets_tags %}"
        "{% render_block_assets required_file_extension='.js' %}"
    )

    rendered = template.render(Context({"page": page}))

    assert "test/app.js" in rendered
    assert "test/app.css" not in rendered
