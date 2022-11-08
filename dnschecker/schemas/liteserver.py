from pydantic import BaseModel


class LiteserverId(BaseModel):
    key: str


class Liteserver(BaseModel):
    ip: int
    port: int
    id: LiteserverId
