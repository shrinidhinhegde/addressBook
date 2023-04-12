from math import radians, sin, asin, sqrt, cos

from fastapi import HTTPException, Request, Depends, status
from sqlalchemy.orm import Session

from app.utils import models, database_config
from app.utils.input_schemas import CreateAddressSchema


def validate_coordinates_validator(data: CreateAddressSchema):
    """
    Validator Function to validate the latitude and longitude of an address.
    """
    if not (-90 <= data.lat <= 90) or not (-180 <= data.lng <= 180):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Latitude must be between -90 and 90, and longitude must be between -180 and 180")


def validate_radius(request: Request):
    """
    Function to validate the radius of a search.
    """
    for key, val in request.query_params.items():
        if key == "radius":
            radius = float(val)
            if not 0 < radius <= 6371:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Radius is invalid.")


def address_exists(request: Request, db: Session = Depends(database_config.get_db)):
    """
    Function to check if an address exists.
    """
    address_id = None
    for key, val in request.path_params.items():
        if key == "address_id":
            address_id = val
    if not address_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="dataset_id not found")
    address = db.query(models.Address).where(models.Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address does not exist")


def is_within_radius(lat1, lon1, lat2, lon2, radius) -> bool:
    """
    Function to check if two points are within a certain radius of each other.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  # convert decimal degrees to radians

    # haversine formula
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance = 6371 * c

    return distance <= radius
