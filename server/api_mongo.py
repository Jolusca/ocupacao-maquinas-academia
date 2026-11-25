import os
import asyncio

from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

db_username = os.getenv("MONGODB_USERNAME", "")
db_password = os.getenv("MONGODB_PASSWORD", "")
db_uri = os.getenv("MONGODB_URI", "")

async def health():
    uri = f"mongodb+srv://{db_username}:{db_password}@ocupacaomaquinas.wsoskab.mongodb.net/" or db_uri
    client = AsyncMongoClient(uri)

    await client.admin.command("ping")
    print("Connected successfully")
    await client.close()
    
# async def insert_data():
    

asyncio.run(health())