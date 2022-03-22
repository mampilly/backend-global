from __future__ import annotations
import datetime
from typing import List

import logging
from fastapi import APIRouter, Depends, Query
from app.core.auth import get_current_user
from app.ratelimit.time_bucketed import rate_limit
from app.routes.businesses.service.business_trends.business_trends_service import BusinessTrendsService
from app.exceptions.application_exception import exception
from app.core.enum.date_filter import DATEFILTER
from app.routes.businesses.service.business_trends.dto.bsi_trend_output import BsiTrendOutput
from app.routes.businesses.service.business_trends.dto.watch_level_trend_output import WatchLevelTrendOutput
from app.routes.businesses.service.business_trends.dto.stock_price_trend_output import StockPriceTrendOutput
from app.routes.businesses.service.business_trends.dto.bsi_vs_stock_correlation_output import CorrelationTrendOutput
from app.routes.businesses.service.business_trends.dto.average_sentiment_trend_output import AverageSentimentTrendOutput
from app.routes.businesses.service.business_trends.dto.sentiment_distribution_trendoutput import SentimentDistributionTrendOutput
from app.routes.businesses.service.business_trends.dto.platform_index_trend_output import PlatformIndexTrendOutput
from app.routes.businesses.service.business_trends.dto.redflag_trend_output import RedflagTrendOutput

router = APIRouter(prefix="/business-trend")
CALLS = 900
PERIOD = 900


@router.get("/bsi-score", tags=["Business Trends"], response_model=List[BsiTrendOutput])
async def bsi_score_trend(
    business_id: int,
    time_period: str = Query(
        ...,  enum=DATEFILTER.date_filter),
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the media presence of the company on a monthly basis. This is calculated using the ‘Business Sentiment Index’ formula.

    - **business_id**: unique id of the business
    - **time_period**: Last Year, Last 6 Months or Current Month
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id,
            'date': time_period,
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.get_bsi_trend(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/watch-level", tags=["Business Trends"], response_model=List[WatchLevelTrendOutput])
async def watch_level_trend(
    business_id: int,
    time_period: str = Query(
        ...,  enum=DATEFILTER.date_filter),
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the change in the watch level for the company over a given period of time. Watch Levels can be categorized into different types based on ‘Business Sentiment Index’.

    - **business_id**: unique id of the business
    - **time_period**: Last Year, Last 6 Months or Current Month
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id,
            'date': time_period,
            'account_id': int(auth.account_id)
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.get_watch_level_trend(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/stock-price", tags=["Business Trends"], response_model=List[StockPriceTrendOutput])
async def stock_price_trend(
    business_id: int,
    time_period: str = Query(
        ...,  enum=DATEFILTER.date_filter),
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the BSI trend against split-adjusted stock price value.

    - **business_id**: unique id of the business
    - **time_period**: Last Year, Last 6 Months or Current Month
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id,
            'date': time_period,
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.get_stock_price_trend(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/correlation-bsi-vs-stockprice", tags=["Business Trends"], response_model=CorrelationTrendOutput)
async def correlation_bsi_vs_stockprice(
    business_id: int,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the following details of the given company:
    - **Same-Day Correlation**: BSI value correlated with the same day stock price value.
    - **Next-Day Correlation**: BSI value correlated with the next day stock price value.
    - **7-Day Lagged Correlation**: BSI value correlated with the stock price value 7 days later.
    - **14-Day Lagged Correlation**: BSI value correlated with the stock price value 14 days later.
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.correlation_bsi_vs_stockprice(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/average-sentiment", tags=["Business Trends"], response_model=List[AverageSentimentTrendOutput])
async def average_sentiment_trend(
    business_id: int,
    time_period: str = Query(
        ...,  enum=DATEFILTER.date_filter),
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the monthly average sentiment for the company over the selected period of time.

    - **business_id**: unique id of the business
    - **time_period**: Last Year, Last 6 Months or Current Month
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id,
            'date': time_period,
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.get_average_sentiment(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/sentiment-distribution", tags=["Business Trends"], response_model=List[SentimentDistributionTrendOutput])
async def sentiment_distribution_trend(
    business_id: int,
    time_period: str = Query(
        ...,  enum=DATEFILTER.date_filter),
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the monthly sentiment distribution for the company over the selected period of time. Sentiment are categorized into positive, neutral and negative.

    - **business_id**: unique id of the business
    - **time_period**: Last Year, Last 6 Months or Current Month
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id,
            'date': time_period,
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.get_sentiment_distribution(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/platform-index", tags=["Business Trends"],  response_model=List[PlatformIndexTrendOutput])
async def platform_index_trend(
    business_id: int,
    time_period: str = Query(
        ...,  enum=DATEFILTER.date_filter),
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the media presence of the company (Platform level) on a monthly basis. This is calculated using the ‘Business Sentiment Index’ formula.

    - **business_id**: unique id of the business
    - **time_period**: Last Year, Last 6 Months or Current Month
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id,
            'date': time_period,
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.get_platform_index_trend(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/redflag", tags=["Business Trends"], response_model=List[RedflagTrendOutput])
async def redflag_trend(
    business_id: int,
    time_period: str = Query(
        ...,  enum=DATEFILTER.date_filter),
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the number of occurrences of certain flagged phrases in the company’s media and news feeds during the selected time period.

    - **business_id**: unique id of the business
    - **time_period**: Last Year, Last 6 Months or Current Month
    \f
    :param item: User input.
    """
    try:
        params = {
            'business_id': business_id,
            'date': time_period,
            'account_id': int(auth.account_id)
        }
        rate_limit(auth.client_id, CALLS, PERIOD)
        return BusinessTrendsService.get_redflag_trend(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()
