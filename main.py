from functools import reduce
import logging
from uuid import uuid4
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

from models.offer import OfferModel
from utils.doc import Doc
from utils.layouts import Layout, LayoutPack, LayoutSweet
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

    def get_layout_model(ItemModel: Sweet | Pack):
        if ItemModel == Sweet:
            return LayoutSweet(image_url=offer.layouts["sweet"])
        elif ItemModel == Pack:
            return LayoutPack(image_url=offer.layouts["pack"])
        raise RuntimeError("Requesting unknown layout")

    def add_item(item: Sweet):
        layout = get_layout_model(type(item))
        page = doc.get_last_page(type(layout))
        if not page or not page.add_item(item):
            doc.add_page(layout)
            add_item(item)

    for model in offer.packs:
        add_item(Pack(model))

    for model in offer.sweets:
        add_item(Sweet(model))

    pagesAmount = len(doc.pages)
    sweetsAmount = 0
    for sweet in offer.sweets:
        sweetsAmount += sweet.amount

    for idx, page in enumerate(doc.pages):
        page.draw_numerator(idx + 1, pagesAmount)
        if type(page) == LayoutSweet:
            page.draw_weight(offer.weight)
            page.draw_price(offer.price)
            page.draw_amount(sweetsAmount)

    return FileResponse(doc.save(uuid4()))
