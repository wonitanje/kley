import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse

from models.offer import OfferConfig, OfferModel
from models.sweet import SweetModel
from router.offer import create_offer

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
def post_offer(body: OfferModel):
    return FileResponse(create_offer(body))


# for test
# if __name__ == "__main__":
#     offer = OfferModel(
#         packs=[],
#         attachments=[],
#         sweets=[
#             SweetModel(
#                 name="123",
#                 description="123",
#                 organization="123",
#                 weight=50,
#                 amount=4,
#                 image_url="./assets/123.jpg",
#             )
#         ],
#         layouts={"sweet": "./assets/sweet-bg.png"},
#         config=OfferConfig(
#             format="image/png",
#             branding=False,
#             until_date="31.12.2024",
#             delivery_date=["31.12.2024", "31.12.2024"],
#             payment_term="100%",
#         ),
#         weight=200,
#         price=531,
#     )
#     create_offer(offer)
