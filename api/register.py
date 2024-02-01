from typing import Union
from fastapi import  Body,APIRouter,Response,status
from models import register

Status=status
router = APIRouter()



@router.post('/register/cars')
async def registercars(response:Response,id:Union[str, None] = Body(default=None),brand:Union[str, None] = Body(default=None),
                     model:Union[str, None] = Body(default=None), 
                     year:Union[int, None] = Body(default=None),
                     photo:Union[str, None] = Body(default=None), 
                     right_view:Union[str, None] = Body(default=None), 
                     left_view:Union[str, None] = Body(default=None),
                     back_view:Union[str, None] = Body(default=None),
                     luxury:Union[bool, None] = Body(default=None), 
                     registration_plate:Union[str, None] = Body(default=None), 
                     seater:Union[int, None] = Body(default=None), 
                     type:Union[str, None] = Body(default=None),
                     Location:Union[str, None] = Body(default=None)):
    try:
    
        res =await register.registercars(id,brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater,type,Location)
        if res=='car registered successfully':
            return {"message":res}
            
        else:
            
            response.status_code = Status.HTTP_400_BAD_REQUEST
            return {"error":res}
    except Exception as error:
        print(error)


@router.post('/register/accept/reject')
async def accrejcars(response:Response,id:Union[str, None] = Body(default=None) ,status:Union[str, None] = Body(default=None)):
    try:
    
        res =await register.accrejcars(id,status)
        if res=='request accepted' and 'request rejected':
            return {"message":res}
            
        else:
            
            response.status_code = Status.HTTP_400_BAD_REQUEST
            return {"error":res}
    except Exception as error:
        print(error)
