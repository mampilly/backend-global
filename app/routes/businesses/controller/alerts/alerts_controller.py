"""Alerts Controller"""
from __future__ import annotations
from app.routes.businesses.controller import alerts
from fastapi import APIRouter, Depends
from typing import List
import logging
from app.core.auth import get_current_user
from app.ratelimit.time_bucketed import rate_limit
from app.routes.businesses.service.alerts.dto.alerts_output import AlertsOutput
from app.routes.businesses.service.alerts.alerts_service import AlertsService
from app.exceptions.application_exception import exception
import datetime
from dateutil.relativedelta import relativedelta
router = APIRouter(prefix="/business-alerts")
CALLS = 900
PERIOD = 900
end = datetime.date.today().isoformat()
start = (datetime.date.today() - relativedelta(months=+1)).isoformat()


@router.get("", tags=["Business Alerts"], response_model=List[AlertsOutput])
async def business_alerts(start_date: datetime.date = start, end_date: datetime.date = end,
                          auth: Depends = Depends(get_current_user),
                          ):
    """
    Shows the alert details from start date to end date.

    - **start_date**: from date of the alerts
    - **end_date**: to date of the alerts
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'account_id': int(auth.account_id)
        }
        return AlertsService.get_alerts(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()
