import datetime
from typing import Union
from fastapi import  Body,APIRouter, Depends, HTTPException, Request,Response,status
from fastapi.responses import JSONResponse

from models import cars

Status=status
router = APIRouter()



@router.post('/car/creation')
async def createcar(response:Response,brand:Union[str, None] = Body(default=None),
                     model:Union[str, None] = Body(default=None), 
                     year:Union[str, None] = Body(default=None),
                     photo:Union[str, None] = Body(default=None), 
                     right_view:Union[str, None] = Body(default=None), 
                     left_view:Union[str, None] = Body(default=None),
                     back_view:Union[str, None] = Body(default=None),
                     luxury:Union[str, None] = Body(default=None), 
                     registration_plate:Union[str, None] = Body(default=None), 
                     seater:Union[str, None] = Body(default=None), 
                     available:Union[str, None] = Body(default=None), 
                     status:Union[str, None] = Body(default=None), 
                     rent:Union[float, None] = Body(default=None), 
                     type:Union[str, None] = Body(default=None),
                     location:Union[str, None] = Body(default=None), 
                     third_party:Union[float, None] = Body(default=None), 
                     full_insurance:Union[float, None] = Body(default=None)):
    try:
    
        res =await cars.createcars(brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, available, status, rent, type,location, third_party, full_insurance)
        if type(res)==dict:
            return res
            
        else:
            
            response.status_code = Status.HTTP_400_BAD_REQUEST
            return {"error":res}
    except Exception as error:
        print(error)





@router.get('/car/{id}')
async def carbyid(id:str ):
    try:
       
        result =await cars.carsbyid(id)
        
        return result
        
        
    except Exception as error:
        print(error)



@router.post('/car/update')
async def update_car(id:Union[str, None] = Body(default=None),
    photo:Union[str, None] = Body(default=None), right_view:Union[str, None] = Body(default=None), left_view:Union[str, None] = Body(default=None),
      back_view:Union[str, None] = Body(default=None) ,available:Union[bool, None] = Body(default=None), status:Union[str, None] = Body(default=None), rent:Union[float, None] = Body(default=None)
    ,location:Union[str, None] = Body(default=None), 
                     third_party:Union[float, None] = Body(default=None), 
                     full_insurance:Union[float, None] = Body(default=None)):
    try:
       
        result =await cars.update_cars(id,photo, right_view, left_view, back_view, available, status, rent,photo, right_view, left_view, back_view, available, status, rent, location, third_party, full_insurance)
        return result
        
    except Exception as error:
        print(error)   
#----------------------------------------------------------------------------------

from aioredis import Redis, create_redis_pool


REDIS_URL = "redis://127.0.0.1"
redis_pool: Redis = None

async def get_redis_pool():
    global redis_pool
    if redis_pool is None:
        redis_pool = await create_redis_pool(REDIS_URL)
    return redis_pool

@router.on_event("shutdown")
async def close_redis_pool():
    if redis_pool is not None:
        redis_pool.close()
        await redis_pool.wait_closed()


@router.get("/")
async def read_root(redis: Redis = Depends(get_redis_pool)):
    cached_data = await redis.get("cached_data")
    if cached_data:
        return {"message": "Data from Redis Cache", "data": cached_data.decode("utf-8")}
    else:
       
        data_to_cache = "Some data to cache"
      
        await redis.setex("cached_data", 60, data_to_cache)
        return {"message": "Data not in cache, processed and stored", "data": data_to_cache}

async def get_etag():
    current_time = datetime.datetime.utcnow().isoformat()
    return f"my_etag_{current_time}"

@router.get("/protected-resource")
async def get_protected_resource(request: Request,etag: str = Depends(get_etag)):
 
    if etag == request.headers.get("If-None-Match"):
        raise HTTPException(status_code=304)

    response_content = {"message": "This is a protected resource"}
    response_headers = {"ETag": etag, "Current-Time": datetime.datetime.utcnow().isoformat()}
    
    return JSONResponse(content=response_content, headers=response_headers)