
from typing import Union
from fastapi import  APIRouter, Body, HTTPException,status

from app import app
from models import config
Status=status
router = APIRouter()


@router.post("/config/")
async def cretae_config(name:Union[str, None] = Body(default=None),value:Union[str, None] = Body(default=None)):
    
    
    configs = await config.config( name,value)
    return configs
    

@router.post("/update_config/{id}")
async def update_config(id:str, name:Union[str, None] = Body(default=None),value:Union[list, None] = Body(default=None)):
    
    
    update_config_result = await config.updateconfig(id, name,value)
   
    
    if "err" in update_config_result:
        raise HTTPException(status_code=422, detail=update_config_result)
    else:
       
        
        for record in app.state.config:
            if id==str(record["id"]):
                record["confvalues"][name]=value
            
        return update_config_result