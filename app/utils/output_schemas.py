from pydantic import BaseModel


class DefaultErrorSchema(BaseModel):
    message: str


class AddressSchema(BaseModel):
    id: str
    lat: float
    lng: float

    class Config:
        orm_mode = True
