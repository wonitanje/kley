from pydantic import BaseModel


class TextConfig(BaseModel):
    margin: float
    resolution: tuple[float, float]
    position: tuple[float, float]
    size: float
