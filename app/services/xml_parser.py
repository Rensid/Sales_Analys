from typing import List, TextIO
import xml.etree.ElementTree as ET
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.base import main_db_manager
from app.models import Product
from app.schemas import Products
from app.logger import log_decorator


@log_decorator
async def parse_product_data(file: TextIO):
    try:
        root = ET.fromstring(await file.read())

    except ET.ParseError as e:
        raise ValueError(f"Failed to parse XML: {e}")
    date = root.attrib.get('date')
    if date is None:
        raise ValueError("Missing 'date' attribute in the XML.")
    products = []
    for product in root.findall('products/product'):
        try:
            product_data = {item.tag: item.text for item in product}
            product_data['date'] = date
            products.append(Products(**product_data))
        except TypeError as e:
            print(f"Error processing product: {e}")
    return {'products': products, 'date': date}


@log_decorator
async def load_products(products: List[Products],
                        session: AsyncSession = Depends(main_db_manager.get_async_session)):
    try:
        session.add_all([Product(**product.dict()) for product in products])
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        session.rollback()
        return {"error": e}
