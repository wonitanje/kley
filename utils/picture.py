from PIL import Image

from utils.service import get_bytes


class Picture:
    def __init__(self, image_url: str) -> None:
        try:
          self.image = Image.open(get_bytes(image_url))
        except:
          self.image = Image.open('assets/no-image.webp')
        self.source = image_url

    def save(self, name: str):
        return self.image.save(f"results/{name}")

    def resize(self, size: tuple[int]):
        width, height = size
        resolution = width / height
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

        newImg = self.image.resize((int(width), int(height)), resample=0)
        self.image.close()

        self.image = newImg
        self.image.load()

        return self.image

    def close(self):
        self.image.close()
