from app import app, on_startup
from api import customers,cars,register,reservation,users
from db import Database,Database1


app.include_router(customers.router,tags=["customer"])
app.include_router(users.router,tags=["users"])
app.include_router(cars.router,tags=["cars"])
app.include_router(register.router,tags=["register"])
app.include_router(reservation.router,tags=["reservation"])

app.add_event_handler("startup", on_startup)