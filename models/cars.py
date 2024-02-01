from db import Database



db=Database()


async def createcars(brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, available, status, rent, type, location, third_party, full_insurance):
    try:
        
        async with db.pool.acquire() as connection:
                async with connection.transaction():
                    

                    cars = await connection.fetch(
                        """
                        INSERT INTO public.cars(
	brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, available, status, rent, type, location, third_party, full_insurance)
	VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17)
                        RETURNING id
                        """,
                        brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, available, status, rent, type, location, third_party, full_insurance
                    )


                    return {
                        "success": True,
                         "id":cars[0]["id"],
                        "brand":brand, "model":model, "year":year, "photo":photo, "right_view":right_view, "left_view":left_view, "back_view":back_view, "luxury":luxury, "registration_plate":registration_plate, "seater":seater, "available":available, "status":status, "rent":rent, "type":type,
                         "location":location, "third_party":third_party, "full_insurance":full_insurance
                       
                    }

    except Exception as error:
        print(f"Error creating cars: {error}")
        


      



       

async def update_cars(id,photo, right_view, left_view, back_view, available, status, rent, location, third_party, full_insurance):
    """
    Update car information in the database.

    Returns:
        str: A message indicating the success or failure of the update operation.
    """
   
    update_data = {
        photo, right_view, left_view, back_view, available, status, rent, location, third_party, full_insurance
    }

    # Filter out None values
    update_data = {key: value for key, value in update_data.items() if value is not None}

    # Check if there are valid fields to update
    if not update_data:
        return "No valid fields to update."

    # Construct the update query
    set_values = ", ".join([f"{col} = ${i + 2}" for i, col in enumerate(update_data.keys())])
    update_query = f"""
        UPDATE public.cars
        SET {set_values}
        WHERE id = $1
        RETURNING id
    """

    try:
        # Execute the update query
        async with db.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(update_query, id, *update_data.values())
                return f"Car with ID {result[0]['id']} updated successfully."

    except Exception as error:
        # Handle errors and provide an error message
        print(f"Error updating cars: {error}")
        return "An error occurred while updating the cars."





        
async def carsbyid(id:str):

    try:    
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                    
                    user = await conn.fetch("""SELECT id, brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, available, status, rent, type, crdat, updat, location, third_party, full_insurance
	FROM public.cars where id=$1""", id)
                    return user
                    
    except Exception as error :
        print(str(error))



async def all_cars(brand,model,seater,available,luxury,type,year,location ):

    conditions = {
        brand,model,seater,available,luxury,type,year,location
    }
    update_data = {key: value for key, value in conditions.items() if value is not None}

    # Check if there are valid fields to update
    if not update_data:
        update_data ={}
    else:
        select_query = """
        SELECT id, brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, available, status, rent, type, crdat, updat, location, third_party, full_insurance
	FROM public.cars
        WHERE available=true and {}
    """.format(" AND ".join(f"{key} = ${i+1}" for i, key in enumerate(update_data)))


    try:
        # Execute the update query
        async with db.pool.acquire() as connection:
            async with connection.transaction():
                
                if update_data=={}:
                    result = await connection.fetch("""SELECT id, brand, model, year, photo, right_view, left_view, back_view, luxury, registration_plate, seater, available, status, rent, type, crdat, updat, location, third_party, full_insurance
	FROM public.cars WHERE available=true and location=$1""",location)
                else:
                    result = await connection.fetch(select_query, *conditions.values())
                    
                return result

    except Exception as error:
        # Handle errors and provide an error message
        print(f"Error  cars: {error}")
        return "An error occurred while getting all cars."