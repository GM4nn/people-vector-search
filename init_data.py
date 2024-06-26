import asyncio
import random
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Link, WriteRules, init_beanie

import pandas as pd

from models import Person, Product
from settings import settings

from bson.dbref import DBRef

def str_to_float(value):
    value = value.replace('$','').replace('.', '').replace(',00', '.').replace(',','.')
    return value


def random_products_ids(products_ids: list):
    
    n_products = random.randint(1, 10)

    products_random_ids = []
    for _ in range(1, n_products + 1):
        random_product_id = products_ids[random.randint(0, len(products_ids) - 1)]
        products_random_ids.append(random_product_id)
    print(f"products_random_ids {products_random_ids}")
    return products_random_ids


async def load_products():
    products_data = pd.read_csv('data\products.csv')
    products_data.fillna('', inplace=True)
    
    dict_list = products_data.to_dict('records')
    products = []
    
    for row in dict_list:
        product = Product(
            id = row['id'],
            ean = row['original_ean'],
            name = row['original_name'],
            description = row['original_description'],
            current_price = str_to_float(row['current_price']),
            promo_price = str_to_float(row['promo_price']),
        )
        
        products.append(product)
    
    return await Product.insert_many(products, link_rule=WriteRules.DO_NOTHING)

async def load_people(products_ids):
    
    people = []

    people_data = pd.read_csv('data\people.csv')
    dict_list = people_data.to_dict('records')
    
    people_exists = await Person.find().to_list()

 
    if len(people_exists) == 0:
        for row in dict_list:
     
            product_links = [
                Link(
                    DBRef(
                        collection='products',
                        database=settings.MONGO_DB,
                        id=id
                    ), Product
                ) 
                for id in random_products_ids(products_ids)
            ]

            person = Person(
                id=row['User Id'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                gender=row['Sex'],
                email=row['Email'],
                phone=row['Phone'],
                birth_date=row['Date of birth'],
                job_title=row['Job Title'],
                products=product_links
            )
            
            people.append(person)

        await Person.insert_many(people, link_rule=WriteRules.DO_NOTHING)

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

    products = await load_products()
    products_ids = list(products.inserted_ids)
    await load_people(products_ids)

    """
    person = await Person.get('751cD1cbF77e005')
    print(person.first_name)
    for product_link in person.products:
        product = await product_link.fetch()
        print(f" - {product.name} (EAN: {product.ean}, Precio: {product.current_price}, Precio promocional: {product.promo_price})")
    """
if __name__ == '__main__':
    asyncio.run(init())