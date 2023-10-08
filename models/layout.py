from pydantic import BaseModel
import utils.constants as const


class LayoutConfig(BaseModel):
    width: int = 3508
    height: int = 2480
    padding: tuple[int, int, int, int] = [170, 220, 170, 120]
    image_url: str = "assets/bg.png"
