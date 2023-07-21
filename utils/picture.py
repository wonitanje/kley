from PIL import Image

from utils.service import get_bytes


class Picture:
    def __init__(self, image_url: str) -> None:
        self.image = Image.open(get_bytes(image_url)).convert("RGBA")

    def save(self, name: str):
        return self.image.save(f"results/{name}")

    def resize(self, width: int, height: int, resolution: float):
        img_w, img_h = self.image.size
        img_resolution = img_w / img_h
        if img_resolution == 1:
            width = height = min(width, height)
        elif img_resolution != resolution:
            if img_resolution < 1:
                new_width = int(height * img_resolution)
                if new_width > width:
                    height = int(width * img_h / img_w)
                else:
                    width = new_width
            else:
                new_height = int(width * img_h / img_w)
                if new_height > height:
                    width = int(height * img_resolution)
                else:
                    height = new_height

        self.image = self.image.resize((int(width), int(height)), resample=0)
        self.image.load()
        return self.image
