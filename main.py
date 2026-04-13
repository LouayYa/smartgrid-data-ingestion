from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from routes import router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# CORS — permissive for development. Tighten in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Create tables on startup (safe no-op if they already exist).
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"service": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(router)
