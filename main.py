from functools import reduce
import logging
from uuid import uuid4
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

from models.offer import OfferModel, Page
from utils.doc import Doc
from utils.layouts import Layout, LayoutPack, LayoutSweet
from utils.layouts.layout_terms import LayoutTerms
from utils.pack import Pack
from utils.sweet import Sweet

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.get("/")
def read_root():
    return "Server is stable"


@app.post("/offer")
def create_offer(offer: OfferModel):
    doc = Doc(config=offer.config)

    def get_page_type(
        page_name: Page,
    ) -> LayoutPack | LayoutSweet | LayoutTerms | Layout:
        return {
            Page.pack: LayoutPack,
            Page.sweet: LayoutSweet,
            Page.terms: LayoutTerms,
        }.get(page_name, Layout)

    def get_page_name(ItemModel: Sweet | Pack):
        page = Page[ItemModel.__name__.lower()]
        if not page:
            raise RuntimeError("Unknown Page")
        return page

    def add_page(page_type: Page):
        Model = get_page_type(page_type)
        image_url = offer.layouts.get(page_type)
        print(f"add_page {page_type=}, {Model=} {image_url=}")
        if not image_url:
            return
        return doc.add_page(Model(image_url))

    def add_item(item: Sweet):
        page_name = get_page_name(type(item))
        Model = get_page_type(page_name)
        page = doc.get_last_page(Model)
        if not page or not page.add_item(item):
            add_page(page_name)
            add_item(item)

    # Info pages
    add_page(Page.introduction)
    add_page(Page.filling)

    # Packs
    for model in offer.packs:
        add_item(Pack(model))

    # Branding
    if offer.config.branding:
        add_page(Page.branding)

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
    for idx, page in enumerate(doc.pages[1:]):
        page.draw_numerator(idx + 2, pagesAmount)
        if type(page) == LayoutSweet:
            page.draw_weight(offer.weight)
            page.draw_price(offer.price)
            page.draw_amount(sweetsAmount)

    return FileResponse(doc.save(uuid4()))
