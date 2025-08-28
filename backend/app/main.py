from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .db.session import Base, engine
from .api import auth, crud, evaluation, dnc, gamification, certificates

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PYMES LMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(crud.router, prefix=settings.api_v1_prefix)
app.include_router(evaluation.router, prefix=settings.api_v1_prefix)
app.include_router(dnc.router, prefix=settings.api_v1_prefix)
app.include_router(gamification.router, prefix=settings.api_v1_prefix)
app.include_router(certificates.router, prefix=settings.api_v1_prefix)


@app.get("/")
def read_root():
    return {"message": "LMS API"}
