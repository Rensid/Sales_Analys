
from app.db.base import main_db_manager
from fastapi import Depends
from app.logger import log_decorator
from settings.config import openai_client
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models import Analys, Product


@log_decorator
async def get_data_for_prompt(date: str,
                              session: AsyncSession = Depends(main_db_manager.get_async_session)):
    date = datetime.strptime(date, '%Y-%m-%d')
    total_revenue = await session.execute(select(func.sum(Product.price * Product.quantity)
                                                 .label("total_revenue"))
                                          .where(Product.date == date))
    top_products = await session.execute(select(Product.name)
                                         .where(Product.date == date)
                                         .order_by(func.sum(Product.price * Product.quantity).desc())
                                         .group_by(Product.name).limit(3))
    categories = await session.execute(select(Product.category)
                                       .group_by(Product.category)
                                       .where(Product.date == date))
    return {'total_revenue': total_revenue.scalar(),
            'top_products': top_products.scalars().all(),
            'categories': categories.scalars().all(), 'date': date}


async def make_prompt(data: dict):
    prompt = f"""
    Пример: Проанализируй данные о продажах за {data['date']}:
    1. Общая выручка: {data['total_revenue']}
    2. Топ-3 товара по продажам: {data['top_products']}
    3. Распределение по категориям: {data['categories']}
    Составь краткий аналитический отчет с выводами и рекомендациями
    """
    return prompt


@log_decorator
async def make_request_to_llm(prompt):

    completion = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion['choices'][0]['message']['content']


@log_decorator
async def load_response_to_db(session: AsyncSession, response):
    analys = Analys(response=response)
    await session.add(analys)
    await session.commit()
