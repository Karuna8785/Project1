from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine, SessionLocal
from app.routers import auth, hr, crm, categories, products
from app.routers.auth import seed_default_roles_and_admin

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Seed initial roles and administrator
with SessionLocal() as db:
    seed_default_roles_and_admin(db)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SmartERP Enterprise Resource Planning System - Collaborative Platform",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Authentication & Module Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(categories.router, prefix=settings.API_V1_STR)
app.include_router(products.router, prefix=settings.API_V1_STR)
app.include_router(hr.router, prefix=settings.API_V1_STR)
app.include_router(crm.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Online",
        "documentation": "/api/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
