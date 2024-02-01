import json
from db import Database1
db=Database1()

async def app_configs():
    # Assuming you have a PostgreSQL connection pool named "pool"
    async with db.pool.acquire() as connection:
        result = await connection.fetch("""
            SELECT
                config.id,
                config.type,
                jsonb_object_agg(confp.cname, confp.cvalue) AS confvalues
            FROM
                config
            JOIN
                confp ON confp.id = config.id
            GROUP BY
                config.id, config.type
        """)
        records_as_dicts = []
        for record in result:
            record_dict = dict(record)
            record_dict['confvalues'] = json.loads(record_dict['confvalues'])
            records_as_dicts.append(record_dict)

    return records_as_dicts



async def updateconfig(id, name, value):
    try:
        async with db.pool.acquire() as connection:
            await connection.execute("UPDATE confp SET cvalue=$3 WHERE id=$1 AND cname=$2", id, name, value)
            return {"message": "Configuration updated successfully."}

    except Exception as error:
        print(f"Error updating configuration: {error}")
        return {"error": "An error occurred while updating the configuration."}


async def config(name, value):
    try:
        async with db.pool.acquire() as connection:
            await connection.execute("select * from setconfig($1,$2)", name, value)
            return {"message": "Configuration created successfully."}

    except Exception as error:
        print(f"Error creating configuration: {error}")
        return {"error": "An error occurred while creating the configuration."}