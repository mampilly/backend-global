from __future__ import annotations
from typing import List
from app.routes.users.services.user.dto.user_details import UserDetailsOutput

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.routes.users.services.user.user_service import UserService
router = APIRouter(prefix="/user")


@router.get("", tags=["User"], response_model=List[UserDetailsOutput])
async def get_user(auth: Depends = Depends(get_current_user),):
    return UserService.get_user_info(auth.user_id)
