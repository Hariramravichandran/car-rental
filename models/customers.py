from db import Database



db=Database()


async def validate_name(name):
        if name==None:
            return "Name cannot be null or undefined."
        if name.strip() == "":
            return "Name cannot be an empty string."
        if name.isspace():
            return "Name cannot consist of spaces only."
        if name.isdigit():
            return "Name cannot be a number."
        if any(char in "!@#$%^&*()_+{}[]:;<>,.?~\\/-" for char in name):
            return "Name cannot contain symbols."
        return "valid"


async def createuser(firstname, lastname, phonenumber, email,guser,address):
    
    chkfname = await validate_name(firstname)
    chklname = await validate_name(lastname)

    if chkfname != "valid":
        return {"err": "err", "error": chkfname}

    if chklname != "valid":
        return {"err": "err", "error": chklname}

    if not phonenumber:
        return {"err": "err", "error": "Phone number required"}

    if not email:
        return {"err": "err", "error": "Email required"}

    try:
        
        async with db.pool.acquire() as connection:
                async with connection.transaction():
                    number_exist = await connection.fetch(
                        'SELECT phonenumber FROM public.customers WHERE phonenumber = $1',
                        phonenumber,
                    )

                    if number_exist!=[]:
                        return {"err": "err", "error": "Phone number already taken"}

                    email_exist = await connection.fetch(
                        'SELECT email FROM public.customers WHERE email = $1',
                        email,
                    )

                    if email_exist!=[]:
                        return {"err": "err", "error": "Email already taken"}


                    user = await connection.fetch(
                        """
                        INSERT INTO public.customers (firstname, lastname, phonenumber, email, guest,address)
                        VALUES ($1, $2, $3, $4, $5,$6)
                        RETURNING id
                        """,
                        firstname,
                        lastname,
                        phonenumber,
                        email.lower(),
                        guser,address
                    )

                    #token =await auth_handler.encode_token(str(user[0]["id"]))

                    return {
                        "success": True,
                         "id": user[0]["id"],
                        #"token": token,
                        "name":firstname +' '+ lastname,
                        "firstname": firstname,
                        "lastname": lastname,
                        "phonenumber": phonenumber,
                        "email": email.lower(),
                        "address":address
                       
                    }

    except Exception as error:
        print(f"Error creating user: {error}")
        



       

async def update_customer(id, firstname, lastname, phonenumber, email,guest,address):
    """
    Update customer information in the database.

    Returns:
        str: A message indicating the success or failure of the update operation.
    """
   
    update_data = {
        "firstname": firstname,
        "lastname": lastname,
        "phonenumber": phonenumber,
        "email": email if email==None else email.lower(),
        "address": address,
        "guest":guest
    }

    # Filter out None values
    update_data = {key: value for key, value in update_data.items() if value is not None}

    # Check if there are valid fields to update
    if not update_data:
        return "No valid fields to update."

    # Construct the update query
    set_values = ", ".join([f"{col} = ${i + 2}" for i, col in enumerate(update_data.keys())])
    update_query = f"""
        UPDATE public.customers
        SET {set_values}
        WHERE id = $1
        RETURNING id
    """

    try:
        # Execute the update query
        async with db.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(update_query, id, *update_data.values())
                return f"Customer with ID {result[0]['id']} updated successfully."

    except Exception as error:
        # Handle errors and provide an error message
        print(f"Error updating customer: {error}")
        return "An error occurred while updating the customer."





        
async def userbyid(user:str):

    try:    
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                    
                    user = await conn.fetch("SELECT id, CONCAT(firstname, ' ', lastname) AS name, email, phonenumber, guest FROM customers where id=$1", user)
                    return user
                    
    except Exception as error :
        print(str(error))


