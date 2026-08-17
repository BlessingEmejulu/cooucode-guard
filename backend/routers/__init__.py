from backend.routers.auth import router as auth_router
from backend.routers.dashboard import router as dashboard_router
from backend.routers.courses import router as courses_router
from backend.routers.submissions import router as submissions_router
from backend.routers.scans import router as scans_router
from backend.routers.comparisons import router as comparisons_router
from backend.routers.reports import router as reports_router
from backend.routers.system import router as system_router

__all__ = [
    "auth_router",
    "dashboard_router",
    "courses_router",
    "submissions_router",
    "scans_router",
    "comparisons_router",
    "reports_router",
    "system_router"
]
