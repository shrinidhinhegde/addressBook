from sqlalchemy import Column, Float, String

from app.utils.database_config import Base


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(String, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    createdAt = Column(String)
    updatedAt = Column(String)
