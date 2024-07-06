from requests import get
from io import BytesIO


def get_bytes(url: str):
    response = get(url)
    return BytesIO(response.content)
