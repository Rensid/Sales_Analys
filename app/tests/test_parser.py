from io import StringIO
import re
from typing import TextIO
import pytest
import aiofiles
from app.schemas import Products
from app.services.xml_parser import load_products, parse_product_data


class AsyncStringIO:
    def __init__(self, initial_value: str):
        self._stringio = StringIO(initial_value)

    async def read(self):
        return self._stringio.read()

    def close(self):
        self._stringio.close()


@pytest.mark.asyncio
async def test_data_parser():
    async with aiofiles.open('data/2.xml', 'rb') as f:
        response = await parse_product_data(f)
    assert isinstance(response, dict)
    assert re.match(
        r'^20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$', response['date'])


@pytest.mark.asyncio
async def test_parse_valid_xml():
    # Создаём тестовый XML
    valid_xml = """
    <sales_data date="2024-01-01">
        <products>
            <product>
                <id>1</id>
                <name>Product 1</name>
                <quantity>100</quantity>
                <price>100</price>
                <category>Category 1</category>
            </product>
            <product>
                <id>2</id>
                <name>Product 2</name>
                <quantity>50</quantity>
                <price>200</price>
                <category>Category 2</category>
            </product>
        </products>
    </sales_data>
    """
    fake_file = AsyncStringIO(valid_xml)

    result = await parse_product_data(fake_file)

    assert result['date'] == "2024-01-01"
    assert len(result['products']) == 2
    assert result['products'][0].name == "Product 1"
    assert result['products'][0].price == 100
    assert result['products'][1].name == "Product 2"
    assert result['products'][1].price == 200


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', ['app/tests/test_data/1.xml',
                                       'app/tests/test_data/2.xml'])
async def test_parse_invalid_xml_and_missing_date(test_data):
    async with aiofiles.open(test_data, 'rb') as f:
        with pytest.raises(ValueError):
            await parse_product_data(f)


@pytest.mark.asyncio
@pytest.mark.parametrize('product',
                         [
                             [Products(**{'name': 'Product 1',
                                       'quantity': 1, 'price': 1.2, 'category': 'Category 1', 'date': '2024-01-01'}),
                              Products(**{'name': 'Product 2',
                                       'quantity': 2, 'price': 2.3, 'category': 'Category 2', 'date': '2024-01-01'}),
                              ],
                             [
                                 Products(**{'name': 'Product 1',
                                             'quantity': 1, 'price': 1.2, 'category': 'Category 1', 'date': '2024-01-02'}),
                                 Products(**{'name': 'Product 2',
                                             'quantity': 2, 'price': 2.3, 'category': 'Category 2', 'date': '2024-01-02'}),
                             ],
                         ]
                         )
async def test_load_products(async_client, product):
    result = await load_products(product)
    assert result["status"] == "success"
