import asyncio
import math
import time
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import WriteRules, init_beanie, BulkWriter

from models import Product
from models import Person
from management_data.embeddings import model
from settings import settings

async def people_embeddings():
    page_size = 500
    offset = 0
    total_documents = await Person.count()
    total_pages = math.ceil(total_documents / page_size)

    
    for page in range(total_pages):
        offset = page * page_size
        
        print(f"PAGE {page}")
        
        async for person in Person.find_all(limit=page_size, skip=offset):

            print(f"EMBEDDING PERSON {person.first_name} - {person.last_name} WITH ID: {person.id}")
            person.first_name_embedding = model.encode([person.first_name])[0].tolist()
            person.last_name_embedding = model.encode([person.last_name])[0].tolist()
            person.email_embedding = model.encode([person.email])[0].tolist()
            person.phone_embedding = model.encode([person.phone])[0].tolist()
            person.birth_date_embedding = model.encode([person.birth_date])[0].tolist()
            person.job_title_embedding = model.encode([person.job_title])[0].tolist()
            # Guardar los cambios en la base de datos
            await person.save(ignore_revision=True, )
        
async def init():
    
    print(settings.MONGO_URI)
    
    # Create Motor client
    client = AsyncIOMotorClient(
        f"{settings.MONGO_URI}/{settings.MONGO_DB}",
    )
    
    models = [
        Product,
        Person
    ]

    # Initialize beanie with the Sample document class and a database
    await init_beanie(database=client.get_default_database(), document_models=models)
    await people_embeddings()

if __name__ == '__main__':
    asyncio.run(init())