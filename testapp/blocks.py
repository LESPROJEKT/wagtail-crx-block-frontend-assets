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
