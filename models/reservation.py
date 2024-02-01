import datetime
from db import Database, Database1
from mail import send_invoice

db=Database()
db1=Database1()

async def createreservation(car_id, customer_id,start_date, end_date, insurance_id,location):
    try:
        
        async with db.pool.acquire() as connection:
                async with connection.transaction():
                    

                    res = await connection.fetch(
                        """
                        select * from reservation($1,$2,$3,$4,$5,$6)
 
                        """,
                        car_id, customer_id,start_date, end_date,location, insurance_id
                    )


                    return 'reservation created'
                        
                       
                    

    except Exception as error:
        print(f"Error creating cars: {error}")
        



       

async def update_reservation(id,car_id,start_date, end_date, return_date, status, insured, insurance_id):
    """
    Update car information in the database.

    Returns:
        str: A message indicating the success or failure of the update operation.
    """
   
    update_data = {
        car_id,start_date, end_date, return_date, status, insured, insurance_id
    }

    # Filter out None values
    update_data = {key: value for key, value in update_data.items() if value is not None}

    # Check if there are valid fields to update
    if not update_data:
        return "No valid fields to update."

    # Construct the update query
    set_values = ", ".join([f"{col} = ${i + 2}" for i, col in enumerate(update_data.keys())])
    update_query = f"""
        UPDATE public.reservation
        SET {set_values}
        WHERE id = $1
        RETURNING id
    """

    try:
        # Execute the update query
        async with db.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(update_query, id, *update_data.values())
                return f"reservation with ID {result[0]['id']} updated successfully."

    except Exception as error:
        # Handle errors and provide an error message
        print(f"Error updating reservation: {error}")
        return "An error occurred while updating the reservation."





        
async def reservationbyid(id:str):

    try:    
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                    
                    user = await conn.fetch("""SELECT id, car_id, customer_id, id_proof, start_date, end_date, rent_cost, insurance_cost, return_date, status, insured, insurance_id, crdat, updat
	FROM public.reservation where id=$1""", id)
                    return user
                    
    except Exception as error :
        print(str(error))



async def cancel_reservation(id:str,cid :str,ctime :datetime):

    try:    
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res=conn.fetch("select * from reservation where id=$1",id)
                if res==[]:
                     return 'there is no reservation for this id'
                else:
                    if res[0]["customer_id"]!=cid:
                         return 'this reservation not made by this user'
                    else:
                        if ctime > res[0]["start_date"]: 
                            await conn.execute("""update reservation set status='canceled' where id=$1 and customer_id =$2 and status='booked'""",id,cid)  

                        
                            return 'reservation canceled'
                             
    except Exception as error :
        print(str(error))        


async def inspection(type,id, inspection_date, status, notes,photo,video):

    try:    
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                    if type=='delivery':
                    
                        await conn.execute("""INSERT INTO public.inspection(
	rental_id, delivery_inspection_date, delivery_status, delivery_notes,  delivery_photo, delivery_video)
	VALUES ($1,$2,$3,$4,$5,$6);""", id, inspection_date, status, notes,photo,video)
                        return 'delevery inspection created'
                    if type ==' return':
                        await conn.execute("""INSERT INTO public.inspection(
	rental_id, return_inspection_date, return_status, return_notes,  return_photo, return_video)
	VALUES ($1,$2,$3,$4,$5,$6);""", id, inspection_date, status, notes,photo,video)
                        
                        check=await conn.fetch('select * from inspection where rentalid=$1',id)
                        if check==[]:
                             return 'inspection error'
                        else:
                            if check[0]["return_status"]==check[0]["delivery_status"]:
                                await conn.execute("update reservation set return_date =select date(current_timestamp)  where id=$1 and status='inrental';",id)
                                datecheck=conn.fetch('select * from reservation where id=$1',id)
                                if datecheck[0]["end_date"]==datecheck[0]["return_date"] or datecheck[0]["end_date"]>datecheck[0]["return_date"]:
                                    main=await conn.execute("""INSERT INTO public.maintenance(
	rental_id, car_id, start_date,status)
	VALUES ($1,$2,(select date(current_timestamp)),'waiting')returning id;""",id,datecheck[0]["car_id"])
                                    await conn.execute("""INSERT INTO public.maintenanceitem(
	id, start_date, title, status)
	VALUES ($1,(select date(current_timestamp)),'water wash','waiting');""",main[0]["id"])
                                    
                                if datecheck[0]["end_date"] < datecheck[0]["return_date"]:
                                    main=await conn.execute("""INSERT INTO public.maintenance(
	rental_id, car_id, start_date,status)
	VALUES ($1,$2,(select date(current_timestamp)),'waiting')returning id;""",id,datecheck[0]["car_id"])
                                    await conn.execute("""INSERT INTO public.maintenanceitem(
	id, start_date, title, status)VALUES ($1,(select date(current_timestamp)),'water wash','waiting');""",main[0]["id"])
                                    
                                    if datecheck[0]["insurance_id"] !=None:
                                        await conn.execute(""""update reservation set total_amount=(
                
                ((SELECT rent FROM cars WHERE id = car_id) * ($2 - $3)) +
                ((
                    SELECT 
                        CASE
                            WHEN (SELECT name FROM insurance WHERE id = $1) = 'Third party' THEN cars.third_party
                            WHEN (SELECT name FROM insurance WHERE id = $1) = 'Full Insurance' THEN cars.full_insurance
                            ELSE NULL
                        END AS selected_value
                    FROM cars WHERE id = car_id
                ) * ($2 - $3))) """,datecheck[0]["insurance_id"],datecheck[0]["return_date"],datecheck[0]["start_date"]
            )
                                    else:
                                         await conn.execute(""""update reservation set total_amount=(
                
                ((SELECT rent FROM cars WHERE id = car_id) * ($2 - $3)) 
                ) """,datecheck[0]["insurance_id"],datecheck[0]["return_date"],datecheck[0]["start_date"]
            )
                                         
                                     






                            if check[0]["return_status"]!=check[0]["delivery_status"]:
                                await conn.execute("update reservation set return_date =select date(current_timestamp) ,status='completed' where id=$1 and status='scheduled';",id)
                                datecheck=conn.fetch('select * from reservation where id=$1',id)
                                if datecheck[0]["end_date"]==datecheck[0]["return_date"] or datecheck[0]["end_date"]>datecheck[0]["return_date"]:
                                    await conn.execute("""INSERT INTO public.incident(
	rental_id, photo, video, description, status)
	VALUES ($1,$2,$3,$4);""",id,photo,video,'refer to maintenence','checking')
                                    
                                    
                                    """main=await conn.execute(INSERT INTO public.maintenance(
	rental_id, car_id, start_date,status)
	VALUES ($1,$2,(select date(current_timestamp)),'waiting')returning id;,id,datecheck[0]["car_id"])
                                    await conn.execute(INSERT INTO public.maintenanceitem(
	id, start_date, title, status)
	VALUES ($1,(select date(current_timestamp)),'water wash','waiting');,main[0]["id"])"""

                                  

                        
                         
               
                    
    except Exception as error :
        print(str(error))


async def idverification(idprof,id,cid):

    try:    
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                    
                    res=await conn.fetch("""SELECT r1.id, r1.car_id, r1.customer_id,CONCAT(c1.firstname, ' ', c1.lastname) AS name,c1.email,c1.phonenumber,r1.start_date, r1.end_date, r1.rent_cost, r1.insurance_cost,r1. insured, r1.insurance_id,r1.total_amount,r1.location
	FROM public.reservation as r1
	join customers as c1 on (c1.id=r1.customer_id)
	where r1.id=$1 and c1.id=$2""",id,cid)
                    if res==[]:
                        return 'id proof verified and car delivered successfully'
                    else:
                        await conn.execute("""update reservation set status='inrental',id_proof=$1 where id=$2 and customer_id=$3""", idprof,id,cid)
                        await conn.execute("""update cars set status='not available',where id=(select car_id from reservation where id=$1) """,id)
                        items = [
        {"Description": "reservation", "Dates":'2024-01-10 -2024-01-14',"totalDates":'5',"price":"50"},
        {"Description": "insurance", "Dates":'2024-01-10 -2024-01-14',"totalDates":'5',"price":"25"},
        
    ] 
                        
                        await send_invoice(res[0]["email"],items,res[0]["name"])
                        return 'id proof verified and car delivered successfully'
                    
                         
               
                    
    except Exception as error :
        print(str(error))