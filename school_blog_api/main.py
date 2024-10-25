from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = AsyncIOMotorClient(os.getenv("MONGODB_CONNECTION_URI"))
db = client.school_blog

@app.on_event("startup")
async def startup_db_client():
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the School Blog API"}


from routes import router as blog_router

app.include_router(blog_router, prefix="/api/v1")