from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List
import logging
from app.core.auth import get_current_user
from app.ratelimit.time_bucketed import rate_limit
from app.routes.businesses.service.business.dto.business_details_output import BusinessDetailsOutput
from app.routes.businesses.service.business.dto.entity_details_output import EntityDetailsOutput
from app.routes.businesses.service.business.dto.business_search_output import BusinessSearchOutput
from app.routes.businesses.service.business.dto.add_business_input import AddBusinessInput
from app.routes.businesses.service.business.business_service import BusinessService
from app.exceptions.application_exception import exception
router = APIRouter(prefix="/business")
CALLS = 900
PERIOD = 900

@router.post("/search", tags=["Business"], response_model=List[BusinessSearchOutput])
async def search_business(business_name: str, website: str,
                          auth: Depends = Depends(get_current_user),
                          ):
    """
    Shows the details of the company.

    - **business_name**: name of the company
    - **website**: website of the company
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_name': business_name,
            'website': website
        }
        return BusinessService.search_business(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/detail", tags=["Business"], response_model=List[BusinessDetailsOutput])
async def company_details(
    business_id: int,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the details of the given company.

    - **business id**: unique id of the company
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
        }
        return BusinessService.get_company_details(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()

@router.get("/entity-detail", tags=["Business"], response_model=List[EntityDetailsOutput])
async def entity_details(
    business_id: int,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the details of the sub entities.

    - **business id**: unique id of the company
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
        }
        return BusinessService.get_entity_details(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()

@router.post("/add-business", tags=["Business"])
async def add_business(
                        business : AddBusinessInput,
                        auth: Depends = Depends(get_current_user),
                      ):
    """
    Adding company to the system and starting data collection.

    - **business_name**: name of the company
    - **website**: website of the company
    - **type**: type of the company
    - **year_founded**: year founded
    - **industry**: industry name of the company
    - **stock_symbol**: stock symbol of the company
    - **address_line_1**: address of the company
    - **address_line_2**: address of the company
    - **city**: city name
    - **state**: state
    - **zip**: zipcode of the country
    - **country**: name of the country
    - **contact_name**: contact of the company
    - **telephone**: telephone number
    - **twitter_handle**: twitter handle of the company
    - **business_alias_name**: business alias name of the company
    - **additional_notes**: additional notes
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_name': business.business_name,
            'address_line_1': business.address_line_1,
            'address_line_2': business.address_line_2,
            'city': business.city,
            'state': business.state,
            'zip': business.zip,
            'country': business.country,
            'type':  business.type,
            'year_founded': business.year_founded,
            'industry': business.industry,
            'stock_symbol': business.stock_symbol,
            'contact_name': business.contact_name,
            'telephone': business.telephone,
            'website': business.website,   
            'twitter_handle': business.twitter_handle,
            'business_alias_name' : '["' + business.business_alias_name + '"]',
            'is_active' : 0,
            'is_new' : 1,
            'additional_notes': business.additional_notes,
            'account_id': int(auth.account_id)
        }
        return BusinessService.add_business(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()
