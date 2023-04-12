import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.utils import database_config, models
from app.utils.error_responses import error_responses
from app.utils.input_schemas import CreateAddressSchema, UpdateAddressSchema
from app.utils.output_schemas import AddressSchema
from app.utils.time_functions import current_utc_time
from app.utils.validators import validate_coordinates_validator, address_exists, is_within_radius, \
    validate_radius

addresses_router = APIRouter(prefix='/addresses', tags=['addresses'])


@addresses_router.post('/', response_model=AddressSchema, description='Create a new address',
                       dependencies=[Depends(validate_coordinates_validator)], responses={400: error_responses[400]})
async def create_address(data: CreateAddressSchema, db: Session = Depends(database_config.get_db)):
    """
    Function to create a new address. This function is called when a POST request is made to the /addresses endpoint.
    The Latitude and Longitude is validated using depends on the router using validate_coordinates.
    """
    new_address_id = str(uuid.uuid4())
    current_time = current_utc_time()
    new_address = models.Address(id=new_address_id, createdAt=current_time, updatedAt=current_time, **data.dict())
    db.add(new_address)
    db.commit()
    return new_address


@addresses_router.get('/', response_model=Page[AddressSchema], description='List all addresses',
                      responses={404: error_responses[404]})
async def list_addresses(db: Session = Depends(database_config.get_db)):
    """
    Function to get all addresses. This function is called when a GET request is made to the /addresses endpoint.
    """
    addresses = db.query(models.Address).all()
    return paginate(addresses)


@addresses_router.get('/{address_id}', response_model=AddressSchema, description='Get an address by id',
                      dependencies=[Depends(address_exists)], responses={404: error_responses[404]})
async def get_address_by_id(address_id: str, db: Session = Depends(database_config.get_db)):
    """
    Function to get an address by id. This function is called when a GET request is made to the /addresses/{address_id}
    endpoint. The address_id is validated using depends on the router using address_exists.
    """
    address = db.query(models.Address).where(models.Address.id == address_id).first()
    return address


@addresses_router.patch('/{address_id}', response_model=AddressSchema, description='Update an address by id',
                        dependencies=[Depends(validate_coordinates_validator), Depends(address_exists)],
                        responses={404: error_responses[404], 400: error_responses[400]})
async def update_address_by_id(address_id: str, data: UpdateAddressSchema,
                               db: Session = Depends(database_config.get_db)):
    """
    Function to update an address by id. This function is called when a PATCH request is made to the
    /addresses/{address_id} endpoint. The Latitude and Longitude is validated using depends on the router using
    validate_coordinates. The address_id is validated using depends on the router using address_exists.
    """

    address = db.query(models.Address).where(models.Address.id == address_id).first()
    excluded_dict = data.dict()
    for attr, value in excluded_dict.items():
        setattr(address, attr, value)
    address.updatedAt = current_utc_time()
    db.commit()
    return address


@addresses_router.delete('/{address_id}', response_model=AddressSchema, description='Delete an address by id',
                         dependencies=[Depends(address_exists)], responses={404: error_responses[404]})
async def delete_address_by_id(address_id: str, db: Session = Depends(database_config.get_db)):
    """
    Function to delete an address by id. This function is called when a DELETE request is made to the
    /addresses/{address_id} endpoint. The address_id is validated using depends on the router using address_exists.
    """
    address = db.query(models.Address).where(models.Address.id == address_id).first()
    db.delete(address)
    db.commit()
    return address


@addresses_router.get('/search/', response_model=Page[AddressSchema],
                      description='List all addresses within a radius in kilometers',
                      dependencies=[Depends(validate_radius)], responses={400: error_responses[400]})
def get_addresses_within_radius(lat: float, lng: float, radius: float, db: Session = Depends(database_config.get_db)):
    """
    Function to search for addresses within a radius. This function is called when a GET request is made to the
    /addresses/search endpoint.
    """
    validate_coordinates_validator(CreateAddressSchema(lat=lat, lng=lng))
    addresses = db.query(models.Address).all()

    # Filter the results to include only addresses within the given radius
    result = []
    for address in addresses:
        if is_within_radius(lat, lng, address.lat, address.lng, radius):
            result.append(address)

    return paginate(result)
