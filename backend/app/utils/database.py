#"mongodb://adminUser:adminPassword@localhost:27017"
"""format to connect with database:
    mongodb://mi_usuario:mi_contraseña@localhost:27017/mi_base_de_datos
"""
"""
    This file contains the database connection.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

#--------------------- VARIABLES -------------------#
host = os.getenv("DBHOST")
port = os.getenv("DBPORT")
user = os.getenv("DBUSER")
pwd = os.getenv("DBPASS")
db_name = os.getenv("DBNAME")

connection_string = f"mongodb://{user}:{pwd}@{host}:{port}"

client = AsyncIOMotorClient(connection_string)
db = client[db_name]
