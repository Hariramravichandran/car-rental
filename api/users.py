from typing import Union
from fastapi import  Body,APIRouter,Response,status
from models import users

Status=status
router = APIRouter()



@router.post('/user/creation')
async def createuser(response:Response,firstname:Union[str, None] = Body(default=None),
                     lastname:Union[str, None] = Body(default=None),
                     email:Union[str, None] = Body(default=None),
                     phonenumber:Union[str, None] = Body(default=None),
                     guser:Union[bool, None] = Body(default=None),
                     address:Union[str, None] = Body(default=None),usertype:Union[str, None] = Body(default=None)):
    try:
    
        res =await users.createuser(firstname, lastname, phonenumber, email,guser,address,usertype)
        if type(res)==dict:
            return res
            
        else:
            
            response.status_code = Status.HTTP_400_BAD_REQUEST
            return {"error":res}
    except Exception as error:
        print(error)





@router.get('/user/{id}')
async def userbyid(id:str ):
    try:
       
        result =await users.userbyid(id)
        
        return result
        
        
    except Exception as error:
        print(error)



@router.post('/user/update')
async def update_user(id:Union[str, None] = Body(default=None),
    firstname:Union[str, None] = Body(default=None),
    lastname:Union[str, None] = Body(default=None),
    phonenumber:Union[str, None] = Body(default=None),
    email:Union[str, None] = Body(default=None),
    address:Union[str, None] = Body(default=None),
    usertype:Union[str, None] = Body(default=None)
    ):
    try:
       
        result =await users.update_user(id, firstname, lastname, phonenumber, email,address)
        return result
        
    except Exception as error:
        print(error)   