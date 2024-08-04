import uuid
from enum import Enum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.base.models import Basket
from core import exceptions

async def retrieve_open_basket_id(
    business_id: uuid.UUID, user_id: uuid.UUID, session: AsyncSession
) -> uuid.UUID:
    """
    Given a business_id and a user_id, this function retrieves the ID of the open basket associated with those
    identifiers. If no open basket is found, it raises a BaseHTTPException with a 400 status code and an error
    message. If a database error occurs, it raises a BaseHTTPException with a 500 status code and an error message.
    """
    try:
        basket = await session.execute(
            select(Basket).where(
                Basket.user_id == user_id,
                Basket.business_id == business_id,
                Basket.status == "open",
            )
        )
        basket = basket.scalars().first()
        if basket:
            return basket.id
        else:
            raise exceptions.BaseHTTPException(
                400,
                "no_open_basket",
                "there is no open basket for the user_id",
            )
    except Exception as e:
        raise exceptions.BaseHTTPException(
            500,
            "database_error",
            f"database error: {str(e)}",
        )

