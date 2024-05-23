# main code.
# The main point of call.
from fastapi import FastAPI
# from schema import *
from db.session import engine
from db import main_model as models
# from apis.client import client_router
from apis.settings_api import settings_router
from apis.users import user_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, asyncio
import os

# Microservice description
description = "Study Gateway Application"
tags_metadata =[
    {
        "name":"Client",
        "description":"Study Gateway Application Crud",
    }
]

study_gate_app = FastAPI(
    title="Study Gateway API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
# create the tables.
models.Base.metadata.create_all(engine)
# allowed host.
origins =[]
study_gate_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

async def main() -> None:
    config = uvicorn.Config(
        "main:study_gate_app", 
        host=os.getenv("HOST"), 
        port=int(os.getenv("ACCESS_PORT")), 
        reload=os.getenv("RELOAD"),
        workers=1, 
        loop="asyncio")
    
    server = uvicorn.Server(config)
    await server.serve()

study_gate_app.mount("/static", StaticFiles(directory="static"), name="static")

<<<<<<< HEAD
=======

>>>>>>> ff7792b112a6e7ba3f314b460586976730b051e2
# include client router.
study_gate_app.include_router(
    settings_router
)

study_gate_app.include_router(
    user_router
)


@study_gate_app.on_event("startup")
async def startup_event():
    pass
      
@study_gate_app.get("/")
async def ping():
    return {"detail": "Study Gateway App is up"}

if __name__ == "__main__":
    # Run the FastAPI app
    asyncio.run(main())