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

    return products_random_ids


async def load_products():
    products_data1 = pd.read_csv('data\products_aurrera.csv')
    products_data1.fillna('', inplace=True)
    
    products_data2 = pd.read_csv('data\products_casa_ley.csv')
    products_data2.fillna('', inplace=True)
    
    products_data3 = pd.read_csv('data\products_heb.csv')
    products_data3.fillna('', inplace=True)
    
    products_data4 = pd.read_csv('data\products_sams.csv')
    products_data4.fillna('', inplace=True)
            
    products_data5 = pd.read_csv('data\products_soriana.csv')
    products_data5.fillna('', inplace=True)
    
    dict_list1 = products_data1.to_dict('records')
    dict_list2 = products_data2.to_dict('records')
    dict_list3 = products_data3.to_dict('records')
    dict_list4 = products_data4.to_dict('records')
    dict_list5 = products_data5.to_dict('records')
    
    dict_list = dict_list1 + dict_list2 + dict_list3 + dict_list4 + dict_list5
    products = []
    
    for row in dict_list:
        product = Product(
            id = row['id'],
            ean = str(row['original_ean']),
            name = row['original_name'],
            description = row['original_description'],
            current_price = str_to_float(row['current_price']),
            promo_price = str_to_float(row['promo_price']),
            store = row['store']
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

            person = Person(
                id=row['User Id'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                gender=row['Sex'],
                email=row['Email'],
                phone=row['Phone'],
                birth_date=row['Date of birth'],
                job_title=row['Job Title'],
                products=random_products_ids(products_ids)
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


if __name__ == '__main__':
    asyncio.run(init())