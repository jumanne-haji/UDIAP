from fastapi import APIRouter
from app.api import auth, assessments, behaviour, reports, analytics, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["Assessments"])
api_router.include_router(behaviour.router, prefix="/behavior", tags=["Behaviour"])
api_router.include_router(reports.router, prefix="/report", tags=["Reports"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
