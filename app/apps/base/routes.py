from typing import Any, Generic, Type, TypeVar

from fastapi import APIRouter, BackgroundTasks, Request

from core.exceptions import BaseHTTPException
from server.config import Settings

# from .handlers import create_dto
from .models import BaseEntity, ## TaskBaseEntity
import app.apps.base.services as services


"""
Based on models developed in app>apps>base>models.py
write CRUP Endpoints with maturity level 2
"""

#### Basket Endpoints ####

##### return list of baskets #####


@router.get(
    "/baskets",
    summary="Get basket list",
    description="Get list of baskets for a user",
    response_model=list[BaseEntity],
)
async def get_basket_list_for_user(
    user_id: uuid.UUID, business_id: uuid.UUID, request: Request
) -> list[BaseEntity]:
    """
    Get basket list for a user

    :param user_id: the uid of the user
    :type user_id: uuid.UUID
    :param business_id: the uid of the business
    :type business_id: uuid.UUID
    :param request: fastapi request object
    :type request: Request
    :return: list of baskets
    :rtype: list[BaseEntity]
    """
    settings = request.app.state.settings
    baskets = await services.base.get_baskets_for_user(
        user_id=user_id, business_id=business_id, settings=settings
    )
    return baskets

##### return current open Basket #####

@router.get(
    "/baskets/open",
    summary="Get open basket for user_id and business_id",
    description="Get list of baskets for a user filtered by open status",
    response_model=list[BaseEntity],
)
async def get_open_basket_for_user_and_business(
    user_id: uuid.UUID, business_id: uuid.UUID, request: Request
) -> list[BaseEntity]:
    """
    Get open basket list for a user and business

    :param user_id: the uid of the user
    :type user_id: uuid.UUID
    :param business_id: the uid of the business
    :type business_id: uuid.UUID
    :param request: fastapi request object
    :type request: Request
    :return: list of open baskets
    :rtype: list[BaseEntity]
    """
    settings = request.app.state.settings
    baskets = await services.base.get_baskets_for_user(
        user_id=user_id, business_id=business_id, settings=settings
    )
    open_baskets = [basket for basket in baskets if basket.status == "open"]
    if open_baskets:
        return open_baskets
    else:
        raise HTTPException(status_code=404, detail="No open basket found")

##### return single basket #####


@router.get(
    "/baskets/{basket_id}",
    summary="Get basket by basket_id and business_id",
    description="Get basket by basket_id and business_id",
    response_model=BaseEntity,
)
async def get_basket_by_basket_id_and_business_id(
    basket_id: uuid.UUID,
    business_id: uuid.UUID,
    request: Request,
) -> BaseEntity:
    """
    Get basket by basket_id and business_id

    :param basket_id: the uid of the basket
    :type basket_id: uuid.UUID
    :param business_id: the uid of the business
    :type business_id: uuid.UUID
    :param request: fastapi request object
    :type request: Request
    :return: basket
    :rtype: BaseEntity
    """
    settings = request.app.state.settings
    basket = await services.base.get_basket_by_basket_id_and_business_id(
        basket_id=basket_id, business_id=business_id, settings=settings
    )
    if basket.business_id != business_id:
        raise HTTPException(
            status_code=400,
            detail="basket does not belong to the business",
        )
    return basket

####### I should change below ##########
##### update basket #####
@router.put(
    "/baskets/{basket_id}",
    summary="Update open basket by basket_id and business_id",
    description="Update an open basket by basket_id and business_id",
    response_model=BaseEntity,
)
async def update_basket_by_basket_id_and_business_id(
    basket_id: uuid.UUID,
    status: Optional[str] = None,
    currency: Optional[str] = None,
    items: Optional[dict[str, int]] = None,
    amount: Optional[int] = None,
    checkout_at: Optional[datetime] = None,
    business_id: uuid.UUID,
    request: Request,
) -> BaseEntity:
    """
    Update basket by basket_id and business_id

    :param basket_id: the uid of the basket
    :type basket_id: uuid.UUID
    :param status: the status of the basket
    :type status: Optional[str]
    :param currency: the currency of the basket
    :type currency: Optional[str]
    :param items: the items in the basket
    :type items: Optional[dict[str, int]]
    :param amount: the amount of the basket
    :type amount: Optional[int]
    :param checkout_at: the time of checkout
    :type checkout_at: Optional[datetime]
    :param business_id: the uid of the business
    :type business_id: uuid.UUID
    :param request: fastapi request object
    :type request: Request
    :return: basket
    :rtype: BaseEntity
    """
    settings = request.app.state.settings
    basket = await services.base.get_basket_by_basket_id_and_business_id(
        basket_id=basket_id, business_id=business_id, settings=settings
    )
    if basket.status != "open":
        raise HTTPException(
            status_code=400,
            detail="basket is not open",
        )
    if status is not None:
        basket.status = status
    if currency is not None:
        basket.currency = currency
    if items is not None:
        basket.items = items
    if amount is not None:
        basket.amount = amount
    if checkout_at is not None:
        basket.checkout_at = checkout_at
    basket = await services.base.update_basket_by_basket_id_and_business_id(
        basket=basket, settings=settings
    )
    return basket


@router.delete(
    "/baskets/{basket_id}",
    summary="Delete basket by basket_id and business_id",
    description="Delete basket by basket_id and business_id",
)
async def delete_basket_by_basket_id_and_business_id(
    basket_id: uuid.UUID,
    business_id: uuid.UUID,
    request: Request,
) -> None:
    """
    Delete basket by basket_id and business_id

    :param basket_id: the uid of the basket
    :type basket_id: uuid.UUID
    :param business_id: the uid of the business
    :type business_id: uuid.UUID
    :param request: fastapi request object
    :type request: Request
    """
    settings = request.app.state.settings
    await services.base.delete_basket_by_basket_id_and_business_id(
        basket_id=basket_id, business_id=business_id, settings=settings
    )

