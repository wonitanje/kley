from pydantic import BaseModel


class TextSizes(BaseModel):
    organization: int = 25
    enum: int = 25
    name: int = 30
    desc: int = 23
    numerator: int = 50
    info: int = 6


class TextConfig(BaseModel):
    margin: float
    resolution: tuple[float, float]
    position: tuple[float, float]
    max_lines: int = 4
    sizes: TextSizes
