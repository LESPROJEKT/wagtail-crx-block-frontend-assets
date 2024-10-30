"""
Create or customize your page models here.
"""
from coderedcms.models import CoderedWebPage

"""
Create or customize your page models here.
"""

from coderedcms.blocks.content_blocks import (  # noqa
    AccordionBlock,
    CardBlock,
    CarouselBlock,
    FilmStripBlock,
    ImageGalleryBlock,
    ModalBlock,
    PriceListBlock,
    ReusableContentBlock,
)
from coderedcms.blocks.html_blocks import (
    ButtonBlock,
    DownloadBlock,
    EmbedGoogleMapBlock,
    EmbedVideoBlock,
    ImageBlock,
    ImageLinkBlock,
    PageListBlock,
    PagePreviewBlock,
    QuoteBlock,
    RichTextBlock,
    TableBlock,
)
from coderedcms.blocks.layout_blocks import CardGridBlock, GridBlock, HeroBlock
from coderedcms.models import CoderedWebPage
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.fields import StreamField

from testapp.blocks import FrontendAssetsBlock

HTML_STREAMBLOCKS = [
    ("text", RichTextBlock(icon="cr-font")),
    ("button", ButtonBlock()),
    ("image", ImageBlock()),
    ("image_link", ImageLinkBlock()),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code",
            form_classname="monospace",
            label=_("HTML"),
        ),
    ),
    ("download", DownloadBlock()),
    ("embed_video", EmbedVideoBlock()),
    ("quote", QuoteBlock()),
    ("table", TableBlock()),
    ("google_map", EmbedGoogleMapBlock()),
    ("page_list", PageListBlock()),
    ("page_preview", PagePreviewBlock()),
]

CUSTOM_STREAMBLOCKS = [
    ("frontend_assets_block", FrontendAssetsBlock()),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + CUSTOM_STREAMBLOCKS + [
    ("accordion", AccordionBlock()),
    ("card", CardBlock()),
    ("carousel", CarouselBlock()),
    ("film_strip", FilmStripBlock()),
    ("image_gallery", ImageGalleryBlock()),
    ("modal", ModalBlock(HTML_STREAMBLOCKS)),
    ("pricelist", PriceListBlock()),
    ("reusable_content", ReusableContentBlock()),
]

LAYOUT_STREAMBLOCKS = [
    (
        "hero",
        HeroBlock(
            [
                ("row", GridBlock(CONTENT_STREAMBLOCKS)),
                (
                    "cardgrid",
                    CardGridBlock(
                        [
                            ("card", CardBlock()),
                        ]
                    ),
                ),
                (
                    "html",
                    blocks.RawHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
    ("row", GridBlock(CONTENT_STREAMBLOCKS)),
    (
        "cardgrid",
        CardGridBlock(
            [
                ("card", CardBlock()),
            ]
        ),
    ),
    (
        "html",

        blocks.RawHTMLBlock(icon="code", form_classname="monospace", label=_("HTML")),
    ),
] + CUSTOM_STREAMBLOCKS

class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    body = StreamField(
        LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"
