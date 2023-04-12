from pydantic import BaseModel


class DefaultErrorSchema(BaseModel):
    message: str


class AddressSchema(BaseModel):
    id: str
    lat: float
    lng: float
    createdAt: str
    updatedAt: str

    class Config:
        orm_mode = True
