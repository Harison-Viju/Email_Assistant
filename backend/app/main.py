from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import emails as emails_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Powered Communication Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emails_router.router, prefix="/api/emails", tags=["emails"]) 

@app.get("/health")
async def health_check():
    return {"status": "ok"}
