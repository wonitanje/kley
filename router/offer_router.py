from uuid import uuid4

from models.offer_model import OfferModel, Page
from utils.doc import Doc
from utils.layouts import Layout, LayoutPack, LayoutSweet, LayoutAttachment, LayoutTerms
from utils.pack import Pack
from utils.sweet import Sweet
from utils.attachment import Attachment


def create_offer(offer: OfferModel):
    def get_page_type(
        page_name: Page,
    ) -> LayoutPack | LayoutSweet | LayoutAttachment | LayoutTerms | Layout:
        return {
            Page.pack: LayoutPack,
            Page.sweet: LayoutSweet,
            Page.attachment: LayoutAttachment,
            Page.terms: LayoutTerms,
        }.get(page_name, Layout)

    def get_page_name(ItemModel: Pack | Sweet | Attachment):
        page = Page[ItemModel.__name__.lower()]
        if not page:
            raise RuntimeError("Unknown Page")
        return page

    def add_page(page_type: Page):
        Model = get_page_type(page_type)
        image_url = offer.layouts.get(page_type)
        if not image_url:
            return
        return doc.add_page(Model(page_type, image_url))

    def add_raw_item(item: Pack | Attachment):
        page_name = get_page_name(type(item))
        Model = get_page_type(page_name)
        doc.add_page(Model(page_type, item.picture.source))

    def add_item(item: Pack | Sweet | Attachment):
        page_name = get_page_name(type(item))
        Model = get_page_type(page_name)
        page = doc.get_last_page(Model)
        if not page or not page.add_item(item):
            add_page(page_name)
            add_item(item)

    doc = Doc(config=offer.config)

    # Title
    add_page(Page.title)

    # Filling
    if len(offer.attachments) > 1:
        add_page(Page.filling)

    # Packs
    for model in offer.packs:
        add_item(Pack(model))

    # Branding
    if offer.config.branding:
        add_page(Page.branding)

    # Attachments
    for model in offer.attachments:
        add_item(Attachment(model))

    # Sweets
    sweetsAmount = 0
    for model in offer.sweets:
        add_item(Sweet(model))
        sweetsAmount += model.amount

    # Terms
    terms = add_page(Page.terms)
    if terms:
        terms.set_util_date(offer.config.until_date)
        terms.set_delivery_date(offer.config.delivery_date)
        terms.set_payment_term(offer.config.payment_term)

    pagesAmount = len(doc.pages)
    for idx, page in enumerate(doc.pages):
        match page.name:
            case Page.title | Page.terms:
                continue

            case Page.sweet:
                page.draw_weight(offer.weight)
                page.draw_price(offer.price, offer.config.draw_no_tax)
                page.draw_amount(sweetsAmount)

        page.draw_numerator(idx + 1, pagesAmount)

    docPath = doc.save(uuid4())
    doc.close()

    return docPath
