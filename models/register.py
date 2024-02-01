from db import Database1,Database



db=Database()
db1=Database1()


async def registercars(id,brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater,type,Location):
    try:
        
        async with db1.pool.acquire() as connection:
                async with connection.transaction():
                    """ln=await connection.fetch('select * from location where id=$1',Location)
                    if ln==[]:
                        return 'location not available now'
                    else:"""
                        
                    await connection.execute(
                        """
                        INSERT INTO public.registercars(
	customer_id,brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, status, type,location_id)
	VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,'requested',$12,$13)
                        """,
                        id,brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, type,Location
                    )


                    return 'car registered successfully'

    except Exception as error:
        print(f"Error register cars: {error}")



async def accrejcars(id ,sts):
    try:
        
        async with db1.pool.acquire() as connection:
                async with connection.transaction():
                    

                    accrejcars = await connection.fetch(
                        """select * from accrejcars($1,$2)""",
                        id,sts
                    )
                    print(accrejcars[0]["accrejcars"])
                    car=await connection.fetch("""SELECT  id,
            brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, type,location_id
        FROM 
            public.registercars 
        WHERE 
            id = $1;""",id)
                    print(car)
                    if accrejcars[0]["accrejcars"]=='request accepted':
                        async with db.pool.acquire() as conn:
                            async with conn.transaction():
                         
                                await conn.execute("""INSERT INTO public.cars(
            id,brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, status, type,location) values($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)"""
        ,car[0]['id'],car[0]['brand'], car[0]['model'], car[0]['year'], car[0]['photo'], car[0]['right_view'], car[0]['left_view'], car[0]['back_view'], car[0]['luxury'], car[0]['registration_plate'], car[0]['seater'],'available', car[0]['type'],car[0]['location_id'])
                        return accrejcars[0]["accrejcars"]                   
                    else:
                        return accrejcars[0]["accrejcars"]
                                     
                    

    except Exception as error:
        print(f"Error accrejcars cars: {error}")  