import traceback

from fastapi import FastAPI
from fastapi import Query, Depends

from dnschecker.schemas.models import DhtNodeModel, DhtResolveModel
from dnschecker.core.checker import DHTChecker
from dnschecker.api.deps import dht_checker_dep
from typing import List

from loguru import logger


api = FastAPI(docs_url='/')


@api.get('/dhts', response_model=List[DhtNodeModel])
async def get_dhts(checker: DHTChecker=Depends(dht_checker_dep)):
    try:
        res = []
        for idx, dht, is_online in checker.dht_status:
            # logger.error(f"{idx}, {dht}, {is_online}")
            res.append(DhtNodeModel.from_dht_node(idx, dht, is_online))
        return res
    except:
        logger.critical(f"METHOD: /dhts. Error: {traceback.format_exc()}")


@api.get('/resolve', response_model=List[DhtResolveModel])
async def get_resolve(adnl: str=Query(..., example='2D7CF7C6238E4E8B7DA16B0707222C3A95C8DB6A8E4FA4F101052306130EEFDC'), 
                      checker: DHTChecker=Depends(dht_checker_dep)):
    try:
        adnl = adnl.upper().strip()
        logger.info(f'/resolve with adnl: "{adnl}"')
        res = checker.check_adnl(adnl)
        return [DhtResolveModel.parse_obj(obj) for obj in res.values()]
    except:
        logger.critical(f"METHOD: /resolve. Error: {traceback.format_exc()}")
    return []    
