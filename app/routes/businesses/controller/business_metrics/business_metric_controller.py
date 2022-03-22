from __future__ import annotations

import logging
import datetime
from fastapi import APIRouter, Depends, params
from typing import List, Optional
from app.core.auth import get_current_user
from app.ratelimit.time_bucketed import rate_limit
from app.routes.businesses.service.business_metrics.business_metric_service import BusinessMetricService
from app.exceptions.application_exception import exception
from app.routes.businesses.service.business_metrics.dto.media_topics_output import MediaTopicsOutput
from app.routes.businesses.service.business_metrics.dto.keywords_output import KeywordsOutput
from app.routes.businesses.service.business_metrics.dto.redflag_output import RedFlagOutput
from app.routes.businesses.service.business_metrics.dto.public_perception_output import PublicPerceptionOutput
from app.routes.businesses.service.business_metrics.dto.entity_details_output import EntityDetailsOutput
from app.routes.businesses.service.business_metrics.dto.sentiment_distribution_output import SentimentDistributionOutput
from app.routes.businesses.service.business_metrics.dto.average_senetiment_output import AverageSenetimentOutput
from app.routes.businesses.service.business_metrics.dto.platform_index_output import PlatformIndexOutput
from app.routes.businesses.service.business_metrics.dto.news_output import NewsOutput
from app.routes.businesses.service.business_metrics.dto.watch_level_metric_output import WatchLevelOutput
from app.routes.businesses.service.business_metrics.dto.bsi_score_metric_output import BsiScoreMetricOutput
router = APIRouter(prefix="/business-metric")
CALLS = 900
PERIOD = 900
start = datetime.date.today().isoformat()


@router.get("/bsi-score", tags=["Business Metrics"], response_model=List[BsiScoreMetricOutput])
async def bsi_score(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the media presence of the company on a given date. This is calculated using the ‘Business Sentiment Index’ formula.

    - **business_id**: unique id of the business
    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date,
        }
        return BusinessMetricService.get_bsi_score(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/watch-level", tags=["Business Metrics"], response_model=WatchLevelOutput)
async def watch_level(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the watch level for the company on a given date. Watch Levels can be categorized into different types based on ‘Business Sentiment Index’.

    - **business_id**: unique id of the business
    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date,
            'account_id': int(auth.account_id)
        }
        return BusinessMetricService.get_watch_level(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/credit-bureau-score", tags=["Business Metrics"], include_in_schema=False)
async def credit_bureau_score(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date
        }
        return BusinessMetricService.get_credit_bureau_score(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/recent-news", tags=["Business Metrics"], response_model=List[NewsOutput])
async def recent_news(
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Lists the most negative business sentiment articles in the given month, in the order of date published.

    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'date': date,
            'account_id': int(auth.account_id)
        }
        return BusinessMetricService.get_recent_news(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/top-news", tags=["Business Metrics"], response_model=List[NewsOutput])
async def top_news(auth: Depends = Depends(get_current_user),
                   ) -> dict[str, int]:
    """
    Lists the most negative business sentiment articles in the past 3 months, in the descending order of sentiment value. 

    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'account_id': int(auth.account_id)
        }
        return BusinessMetricService.get_top_news(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/current-platform-index", tags=["Business Metrics"], response_model=List[PlatformIndexOutput])
async def current_platform_index(
    business_id: int,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the media presence of the company (Platform level) on a given date. This is calculated using the ‘Business Sentiment Index’ formula.

    - **business_id**: unique id of the business
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id}
        return BusinessMetricService.get_current_platform_index(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/average-sentiment", tags=["Business Metrics"], response_model=List[AverageSenetimentOutput])
async def avg_sentiment(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the monthly average sentiment for the company on the given date.

    - **business_id**: unique id of the business
    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date
        }
        return BusinessMetricService.get_avg_sentiment(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/sentiment-distribution", tags=["Business Metrics"], response_model=List[SentimentDistributionOutput])
async def sentiment_distribution(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the monthly sentiment distribution for the company on the given date. Sentiment are categorized into positive, neutral and negative.

    - **business_id**: unique id of the business
    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date
        }
        return BusinessMetricService.get_sentiment_distribution(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/entity-details", tags=["Business Metrics"], response_model=List[EntityDetailsOutput])
async def entity_details(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the entity details of the given company.

    - **business_id**: unique id of the business
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date
        }
        return BusinessMetricService.get_entity_details(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/public-perception", tags=["Business Metrics"], response_model=PublicPerceptionOutput)
async def public_perception(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the emotions expressed by customers in their reviews. The average values for the sentiment data are calculated using the proprietary formula. The data is collected on the selected month.

    - **business_id**: unique id of the business
    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date
        }
        return BusinessMetricService.get_public_perception(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/redflags", tags=["Business Metrics"], response_model=List[RedFlagOutput])
async def redflags(
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the name of certain flagged phrases in the company’s media and news feeds on the give month.

    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'date': date,
            'account_id': int(auth.account_id)
        }
        return BusinessMetricService.get_redflags(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/keywords", tags=["Business Metrics"], response_model=List[KeywordsOutput])
async def keywords(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows the various topics in the reviews mentioned by the customers in the news and media feed on the given month.

    - **business_id**: unique id of the business
    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date
        }
        return BusinessMetricService.get_keywords(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()


@router.get("/media_topics", tags=["Business Metrics"], response_model=List[MediaTopicsOutput])
async def media_topics(
    business_id: int,
    date: Optional[datetime.date] = start,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    """
    Shows a representation of the various topics in the reviews mentioned by the customers in the news and media feed on the given date.

    - **business_id**: unique id of the business
    - **date**: any date. If not given, current date will be taken
    \f
    :param item: User input.
    """
    try:
        rate_limit(auth.client_id, CALLS, PERIOD)
        params = {
            'business_id': business_id,
            'date': date
        }
        return BusinessMetricService.get_media_topics(params)
    except Exception as error:
        logging.error(error)
        raise exception.internal_server_error()
