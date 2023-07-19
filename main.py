from uuid import uuid4
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import FileResponse
from collections import Counter

from models.offer import ChangeOfferModel, OfferModel
from utils.doc import Doc
from utils.layout import Layout
from utils.sweet import Sweet

app = FastAPI()


@app.get("/")
def read_root():
    return "Server is stable"


@app.post("/offer")
def create_offer(offer: OfferModel):
    doc = Doc()

    def add_page():
        doc.add_page(Layout(offer.background))

    def add_sweet(sweet: Sweet):
        print("add_sweet", sweet.name, doc.page)
        return doc.page and doc.page.add_sweet(sweet)

    for name, amount in Counter(offer.sweets).items():
        sweet = Sweet(name, amount)
        if not add_sweet(sweet):
            add_page()
            add_sweet(sweet)
        sweet.picture.dispose()

    pagesAmount = len(doc.pages)
    sweetsAmount = len(offer.sweets)
    for idx, page in enumerate(doc.pages):
        page.draw_weight(offer.weight)
        page.draw_price(offer.price)
        page.draw_amount(sweetsAmount)
        page.draw_numerator(idx + 1, pagesAmount)

    return [FileResponse(path) for path in doc.save(uuid4())]


@app.patch("/offer")
def modify_offer(changes: ChangeOfferModel):
    doc = Doc(changes.file)
    for page in doc.pages:
        if changes.price:
            page.draw_price(changes.price)

    return [FileResponse(path) for path in doc.save(uuid4())]


@app.post("/")
def test(files: list[UploadFile] = File(), price: str = Form()):
    return {"price": price, "files": [file.filename for file in files]}
