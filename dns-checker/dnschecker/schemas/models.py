from pydantic import BaseModel
from typing import Optional


class DhtNodeModel(BaseModel):
    idx: int
    ip: str
    port: int
    key: str
    is_online: bool


class DhtResolveModel(BaseModel):
    ip: Optional[str] = None
    port: Optional[int] = None
