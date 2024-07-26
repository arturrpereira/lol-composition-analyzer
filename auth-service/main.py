from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import public, private


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_origins=["*"],
    allow_headers=["*"],
)


app.include_router(public.router, prefix="/public", tags=["public"])
app.include_router(private.router, prefix="/api", tags=["private"])