"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.database import init_db
from app.config import settings
from app.routers import products, analysis, listing


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="跨境电商选品Agent - AI驱动的精细化选品系统",
    lifespan=lifespan
)

# Include routers
app.include_router(products.router)
app.include_router(analysis.router)
app.include_router(listing.router)


# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    """Serve mobile-friendly UI"""
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }


@app.get("/config")
async def get_config():
    """Get app configuration (non-sensitive)"""
    return {
        "default_markets": settings.default_markets,
        "default_platforms": settings.default_platforms,
        "llm_configured": bool(settings.llm_api_key)
    }
