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


class NestedLayoutBlock(StructBlock):
    content = StreamBlock([("assets", AssetsBlock())], required=False)


class NestedLayoutStreamBlock(StreamBlock):
    layout = NestedLayoutBlock()
    assets = AssetsBlock()


def build_stream_value():
    block = AssetsStreamBlock()
    return block.to_python([{"type": "assets", "value": {"title": "Hello"}}])


def build_duplicate_stream_value():
    block = AssetsStreamBlock()
    return block.to_python(
        [
            {"type": "assets", "value": {"title": "One"}},
            {"type": "assets", "value": {"title": "Two"}},
        ]
    )


def build_nested_stream_value():
    block = NestedLayoutStreamBlock()
    return block.to_python(
        [
            {
                "type": "layout",
                "value": {
                    "content": [{"type": "assets", "value": {"title": "Nested"}}],
                },
            }
        ]
    )


def build_crx_layout_stream_value():
    from coderedcms.blocks.layout_blocks import GridBlock, HeroBlock

    class LayoutStreamBlock(StreamBlock):
        row = GridBlock([("assets", AssetsBlock())])
        hero = HeroBlock([("assets", AssetsBlock())])

    block = LayoutStreamBlock()
    return block.to_python(
        [
            {
                "type": "row",
                "value": {
                    "content": [
                        {
                            "type": "content",
                            "value": {
                                "content": [
                                    {"type": "assets", "value": {"title": "Row"}}
                                ]
                            },
                        }
                    ]
                },
            },
            {
                "type": "hero",
                "value": {
                    "content": [{"type": "assets", "value": {"title": "Hero"}}]
                },
            },
        ]
    )


def render_assets_tag(context, extension=None):
    extension_arg = ""
    if extension is not None:
        extension_arg = f" required_file_extension='{extension}'"
    template = Template(
        "{% load block_assets_tags %}"
        "{% render_block_assets" + extension_arg + " %}"
    )
    return template.render(Context(context))


def test_get_blocks_static_assets_collects_from_mixin():
    assets = get_blocks_static_assets(build_stream_value())
    assert [asset.path for asset in assets] == ["test/app.js", "test/app.css"]


def test_get_blocks_static_assets_collects_from_nested_layouts():
    assets = get_blocks_static_assets(build_nested_stream_value())
    assert [asset.path for asset in assets] == ["test/app.js", "test/app.css"]


def test_get_blocks_static_assets_collects_from_nested_crx_rows_and_heroes():
    assets = get_blocks_static_assets(build_crx_layout_stream_value())
    assert [asset.path for asset in assets] == [
        "test/app.js",
        "test/app.css",
        "test/app.js",
        "test/app.css",
    ]


def test_nested_collection_without_base_layout_block(monkeypatch):
    import wagtail_crx_block_frontend_assets.wagtail_hooks as hooks_mod

    monkeypatch.setattr(hooks_mod, "BaseLayoutBlock", None)

    assets = hooks_mod.get_blocks_static_assets(build_nested_stream_value())
    assert [asset.path for asset in assets] == ["test/app.js", "test/app.css"]

    crx_assets = hooks_mod.get_blocks_static_assets(build_crx_layout_stream_value())
    assert {asset.path for asset in crx_assets} == {"test/app.js", "test/app.css"}


def test_collect_block_assets_attaches_to_request():
    page = SimpleNamespace(body=build_stream_value())
    request = RequestFactory().get("/")

    collect_block_assets(page, request, (), {})

    assert hasattr(request, "block_assets")
    assert {asset.path for asset in request.block_assets} == {
        "test/app.js",
        "test/app.css",
    }


def test_collect_block_assets_dedupes_by_path():
    page = SimpleNamespace(body=build_duplicate_stream_value())
    request = RequestFactory().get("/")

    collect_block_assets(page, request, (), {})

    paths = [asset.path for asset in request.block_assets]
    assert paths.count("test/app.js") == 1
    assert paths.count("test/app.css") == 1
    assert set(paths) == {"test/app.js", "test/app.css"}


def test_render_block_assets_template_tag_renders_required_extension():
    page = SimpleNamespace(body=build_stream_value())
    rendered = render_assets_tag({"page": page}, extension=".js")

    assert "test/app.js" in rendered
    assert "test/app.css" not in rendered


def test_render_block_assets_filters_css():
    page = SimpleNamespace(body=build_stream_value())
    rendered = render_assets_tag({"page": page}, extension=".css")

    assert "test/app.css" in rendered
    assert "test/app.js" not in rendered


def test_render_block_assets_preview_fallback_when_block_assets_missing():
    page = SimpleNamespace(body=build_stream_value())
    request = RequestFactory().get("/")
    rendered = render_assets_tag({"page": page, "request": request})

    assert "test/app.js" in rendered
    assert "test/app.css" in rendered
