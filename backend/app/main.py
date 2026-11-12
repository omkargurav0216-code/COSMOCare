from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.database.init_db import init_db
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title=settings.APP_NAME, version=settings.API_VERSION,
              description="COSMOCare astronaut telemetry and experimental risk API",
              lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail":"Internal server error","type":"internal_error"})

@app.get("/health", tags=["system"])
def health():
    return {"status":"ok","service":"cosmocare-backend","version":settings.API_VERSION}
