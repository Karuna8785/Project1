"""
SmartERP - FastAPI Application Entry Point
Member 2: HR Management Module
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import api_router
from app.database.database import Base, engine

# Create all tables on startup (for development)
# In production, use Alembic migrations instead
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## SmartERP — Enterprise Resource Planning System

    ### Modules
    | Module | Owner | Status |
    |---|---|---|
    | Authentication & Security | Member 1 | Pending Integration |
    | **HR Management** | **Member 2** | ✅ **Implemented** |
    | CRM | Member 3 | Coming Soon |
    | Inventory | Member 4 | Coming Soon |
    | Sales | Member 5 | Coming Soon |
    | Procurement & Finance | Member 6 | Coming Soon |
    | Dashboard & Reports | Member 7 | Coming Soon |
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(api_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "active_modules": ["HR Management (Member 2)"],
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
