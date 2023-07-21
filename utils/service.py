from requests import get


def get_bytes(url: str):
    with open(".tempfile", "wb") as file:
        file.write(get(url).content)
    return ".tempfile"
