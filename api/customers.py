from typing import Union
from fastapi import  Body,APIRouter,Response,status
from models import customers

Status=status
router = APIRouter()



@router.post('/customer/creation')
async def createuser(response:Response,firstname:Union[str, None] = Body(default=None),
                     lastname:Union[str, None] = Body(default=None),
                     email:Union[str, None] = Body(default=None),
                     phonenumber:Union[str, None] = Body(default=None),
                     guser:Union[bool, None] = Body(default=None),
                     address:Union[str, None] = Body(default=None)):
    try:
    
        res =await customers.createuser(firstname, lastname, phonenumber, email,guser,address)
        if type(res)==dict:
            return res
            
        else:
            
            response.status_code = Status.HTTP_400_BAD_REQUEST
            return {"error":res}
    except Exception as error:
        print(error)





@router.get('/customer/{id}')
async def userbyid(id:str ):
    try:
       
        result =await customers.userbyid(id)
        
        return result
        
        
    except Exception as error:
        print(error)



@router.post('/customer/update')
async def update_customer(id:Union[str, None] = Body(default=None),
    firstname:Union[str, None] = Body(default=None),
    lastname:Union[str, None] = Body(default=None),
    phonenumber:Union[str, None] = Body(default=None),
    email:Union[str, None] = Body(default=None),
    address:Union[bool, None] = Body(default=None),
    guest:Union[bool, None] = Body(default=None)
    ):
    try:
       
        result =await customers.update_customer(id, firstname, lastname, phonenumber, email,guest,address)
        return result
        
    except Exception as error:
        print(error)   