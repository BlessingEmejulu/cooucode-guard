import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from backend.config import BASE_DIR, APP_NAME, APP_TITLE, APP_VERSION
from backend.database import engine, Base, SessionLocal, init_db_schema
from backend.services.demo_data import seed_demo_data
from backend.routers import (
    auth_router,
    dashboard_router,
    courses_router,
    submissions_router,
    scans_router,
    comparisons_router,
    reports_router,
    system_router
)

# Initialize database tables & auto-migrations
init_db_schema()

# Seed demo dataset on startup
try:
    with SessionLocal() as db_session:
        seed_demo_data(db_session)
except Exception as e:
    print(f"[COOUCodeGuard] Seed warning: {e}")

# FastAPI Application instance
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="Offline Source Code Plagiarism Detection System for Chukwuemeka Odumegwu Ojukwu University"
)

# Enable CORS for local cross-origin development (VS Code Live Server on port 5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(courses_router)
app.include_router(submissions_router)
app.include_router(scans_router)
app.include_router(comparisons_router)
app.include_router(reports_router)
app.include_router(system_router)

# Mount Frontend Static Assets
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    css_dir = FRONTEND_DIR / "css"
    js_dir = FRONTEND_DIR / "js"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "COOUCodeGuard Backend API is running."}

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    # If API route, return JSON 404
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=404, content={"detail": "API endpoint not found"})
    # Otherwise fallback to index.html for Single Page Application routing
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse(status_code=404, content={"detail": "Not found"})
