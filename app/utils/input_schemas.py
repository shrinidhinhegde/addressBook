from pydantic import BaseModel


class CreateAddressSchema(BaseModel):
    lat: float
    lng: float

    class Config:
        orm_mode = True


class UpdateAddressSchema(BaseModel):
    lat: float
    lng: float

    class Config:
        orm_mode = True


class SearchAddressSchema(BaseModel):
    lat: float
    lng: float
    radius: float

    class Config:
        orm_mode = True
