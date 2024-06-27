import asyncio
import math
import time
from typing import Coroutine
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import WriteRules, init_beanie, BulkWriter

from models import Product
from management_data.embeddings import model
from settings import settings
from beanie.odm.queries.find import FindMany

async def products_embeddings():
    page_size = 500
    offset = 0
    total_documents = await Product.count()
    total_pages = math.ceil(total_documents / page_size)

    
    for page in range(total_pages):
        offset = page * page_size
        
        print(f"PAGE {page}")
        
        products: FindMany[Product] = Product.find_all(limit=page_size, skip=offset)
        
        async for product in products:

            print(f"EMBEDDING PRODUCT {product.name} WITH ID: {product.id}")
            product.name_embedding = model.encode([product.name])[0].tolist()
            if product.ean:
                product.ean_embedding = model.encode([product.ean])[0].tolist()
            
            if product.description:
                product.description_embedding = model.encode([product.description])[0].tolist()

            await product.save(ignore_revision=True)
        
async def init():
    
    print(settings.MONGO_URI)
    
    # Create Motor client
    client = AsyncIOMotorClient(
        f"{settings.MONGO_URI}/{settings.MONGO_DB}",
    )
    
    models = [
        Product,
    ]

    # Initialize beanie with the Sample document class and a database
    await init_beanie(database=client.get_default_database(), document_models=models)
    await products_embeddings()

if __name__ == '__main__':
    asyncio.run(init())