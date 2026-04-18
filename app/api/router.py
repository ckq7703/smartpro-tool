from fastapi import APIRouter
from app.api.endpoints import templates, reports, history, auth

api_router = APIRouter()

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Core Features
api_router.include_router(templates.router, tags=["templates"])
api_router.include_router(reports.router, tags=["reports"])
api_router.include_router(history.router, tags=["history"])
