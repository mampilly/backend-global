from __future__ import annotations
from fastapi import APIRouter
from app.routes.socialmedia.service import social_media_service


router = APIRouter()


@router.get("/instagram", tags=["Social Media"])
async def get_instagram_handle(handle: str):
    return social_media_service.get_recent_posts_instagram(handle)


@router.get("/twitter", tags=["Social Media"])
async def get_twitter_handle(handle: str):
    return social_media_service.get_recent_posts_twitter(handle)
