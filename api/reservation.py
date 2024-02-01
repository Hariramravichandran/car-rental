from datetime import date
import datetime
from io import BytesIO
from typing import Union
from fastapi import  Body,APIRouter, HTTPException,Response,status
from fastapi.responses import FileResponse, PlainTextResponse
from fpdf import FPDF
import requests
from mail import generate_invoice, send_invoice_email
from models import reservation

Status=status
router = APIRouter()



@router.post('/reservation')
async def createuser(response:Response,car_id:Union[str, None] = Body(default=None),
                     customer_id:Union[str, None] = Body(default=None), 
                     start_date:Union[date, None] = Body(default=None), 
                     end_date:Union[date, None] = Body(default=None), 
                     insurance_id:Union[str, None] = Body(default=None),
                     location:Union[str, None] = Body(default=None)
                    ):
    try:
    
        res =await reservation.createreservation(car_id, customer_id,start_date, end_date, insurance_id,location)
        if type(res)==dict:
            return res
            
        else:
            
            response.status_code = Status.HTTP_400_BAD_REQUEST
            return {"error":res}
    except Exception as error:
        print(error)





@router.get('/reservation/{id}')
async def userbyid(id:str ):
    try:
       
        result =await reservation.reservationbyid(id)
        
        return result
        
        
    except Exception as error:
        print(error)



@router.post('/reservation/update')
async def update_customer(id:Union[str, None] = Body(default=None),
    car_id:Union[str, None] = Body(default=None),start_date:Union[date, None] = Body(default=None), end_date:Union[date, None] = Body(default=None), return_date:Union[date, None] = Body(default=None), status:Union[str, None] = Body(default=None),
      insured:Union[bool, None] = Body(default=None), insurance_id:Union[str, None] = Body(default=None)):
    try:
       
        result =await reservation.update_reservation(id,car_id,start_date, end_date, return_date, status, insured, insurance_id)
        return result
        
    except Exception as error:
        print(error)   


@router.post('/reservation/cancel')
async def cancel_reservation(id:Union[str, None] = Body(default=None),customerid:Union[str, None] = Body(default=None),canceltime:Union[date, None] = Body(default=None)):
    try:
       
        result =await reservation.cancel_reservation(id,customerid,canceltime)
        
        return result
        
        
    except Exception as error:
        print(error)     



@router.post('/reservation/inspection')
async def inspection(id:Union[str, None] = Body(default=None),type:Union[str, None] = Body(default=None), inspection_date:Union[str, None] = Body(default=None), status:Union[str, None] = Body(default=None), notes:Union[str, None] = Body(default=None),photo:Union[str, None] = Body(default=None),video:Union[str, None] = Body(default=None)):
    try:
       
        result =await reservation.inspection(type,id, inspection_date, status, notes,photo,video)
        return result
        
        
    except Exception as error:
        print(error) 


@router.post('/reservation/idverification')
async def idverification(id:Union[str, None] = Body(default=None),idproof:Union[str, None] = Body(default=None), customerid:Union[str, None] = Body(default=None)):
    try:
       
        result =await reservation.idverification(idproof,id,customerid)
        return result
        
        
    except Exception as error:
        print(error)         


@router.get("/send_invoice/{email}", response_class=PlainTextResponse)
async def send_invoice(email: str):
    customer_name = "Vijay"  # Replace with actual customer name
    items = [
        {"Description": "reservation", "Dates":'2024-01-10 -2024-01-14',"totalDates":'5',"price":"50"},
        {"Description": "insurance", "Dates":'2024-01-10 -2024-01-14',"totalDates":'5',"price":"25"},
        
    ]  

    try:
        pdf_content =await generate_invoice(customer_name, items)
        await send_invoice_email(email, pdf_content)
        return "Invoice sent successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    


