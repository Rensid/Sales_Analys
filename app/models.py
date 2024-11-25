from sqlalchemy import Date, Integer, String, Column
from app.db.base import main_db_manager


class Product(main_db_manager.Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)


class Analys(main_db_manager.Base):
    __tablename__ = 'analys'

    id = Column(Integer, primary_key=True)
    response = Column(String(1000), nullable=False)
