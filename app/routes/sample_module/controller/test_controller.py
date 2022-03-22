from __future__ import annotations
from fastapi import APIRouter, Depends
from app.routes.sample_module.service.dto.health_check_output import HealthCheckOutput
from app.routes.sample_module.service import test_service
from app.core.auth import get_current_user
CALLS = 900
PERIOD = 900

router = APIRouter()


@router.get("/health", tags=["Health"], response_model=HealthCheckOutput)
async def health_check():
    return test_service.test_req()


@router.get("/testDatabase", include_in_schema=False)
async def test_database():
    return test_service.test_db()


@router.get("sampleReq/{num}", include_in_schema=False)
async def sample_api_a(
    num: int
) -> dict[str, int]:
    return test_service.test_req()


@router.get("/sampleReqAuthorization/{num}", include_in_schema=False)
async def sample_api_b(
    num: int,
    auth: Depends = Depends(get_current_user),
) -> dict[str, int]:
    return test_service.test_req()
