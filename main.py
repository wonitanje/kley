from uuid import uuid4
from fastapi import FastAPI
from fastapi.responses import FileResponse

from models.offer import OfferModel
from utils.doc import Doc
from utils.layout import Layout
from utils.sweet import Sweet

app = FastAPI()


@app.get("/")
def read_root():
    return "Server is stable"


@app.post("/offer")
def create_offer(offer: OfferModel):
    doc = Doc(config=offer.config)

    def add_page():
        doc.add_page(Layout(config=offer.config.layout))

    def add_sweet(sweet: Sweet):
        if len(doc.pages) == 0:
            return False

        return doc.pages[-1].add_sweet(sweet)

    for model in offer.sweets:
        sweet = Sweet(model, config=offer.config.sweet)
        if not add_sweet(sweet):
            add_page()
            add_sweet(sweet)

    pagesAmount = len(doc.pages)
    sweetsAmount = len(offer.sweets)
    for idx, page in enumerate(doc.pages):
        page.draw_weight(offer.weight)
        page.draw_price(offer.price)
        page.draw_amount(sweetsAmount)
        page.draw_numerator(idx + 1, pagesAmount)

    paths = doc.save(uuid4())
    print(paths)
    return [FileResponse(path) for path in paths]
