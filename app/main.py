from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.query import router as query_router
from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(ingest_router, prefix="/ingest", tags=["Ingestion"])
app.include_router(query_router, prefix="/query", tags=["Query"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running"
    }