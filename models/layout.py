from pydantic import BaseModel
import utils.constants as const


class LayoutConfig(BaseModel):
    width: int = const.LAYOUT_WIDTH
    height: int = const.LAYOUT_HEIGHT
    padding: tuple[int, int, int, int]
    image_url: str
