from pydantic import BaseModel
from typing import List


class DhtNodeId(BaseModel):
    key: str


class AdnlAddrUdp(BaseModel):
    ip: int
    port: int


class AdnlAddrList(BaseModel):
    addrs: List[AdnlAddrUdp]
    version: int
    reinit_date: int
    priority: int
    expire_at: int


class DHTNode(BaseModel):
    id: DhtNodeId
    addr_list: AdnlAddrList
    version: int
    signature: str
