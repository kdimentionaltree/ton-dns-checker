from pydantic import BaseModel
from typing import Optional

import socket, struct

from dnschecker.schemas.dht import DHTNode


class DhtNodeModel(BaseModel):
    idx: int
    ip: str
    ip_int: int
    port: int
    key: str
    is_online: bool

    @classmethod
    def from_dht_node(cls, idx, dht: DHTNode, is_online: bool):
        return DhtNodeModel.parse_obj({
            'idx': idx, 
            'ip': socket.inet_ntoa(struct.pack('>i', dht.addr_list.addrs[0].ip)),
            'ip_int': dht.addr_list.addrs[0].ip,
            'port': dht.addr_list.addrs[0].port,
            'key': dht.id.key,
            'is_online': is_online,
        })
        


class DhtResolveModel(BaseModel):
    ip: Optional[str] = None
    port: Optional[int] = None
        
