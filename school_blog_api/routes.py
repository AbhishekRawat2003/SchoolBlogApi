from fastapi import APIRouter, HTTPException
from models import BlogPost
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/posts/", response_description="Create a new blog post", response_model=BlogPost)
async def create_post(post: BlogPost):
    post_dict = jsonable_encoder(post)
    new_post = await db.posts.insert_one(post_dict)
    created_post = await db.posts.find_one({"_id": new_post.inserted_id})
    return created_post

@router.get("/posts/", response_description="List all blog posts", response_model=list[BlogPost])
async def list_posts():
    posts = await db.posts.find().to_list(1000)
    return posts

@router.get("/posts/{post_id}", response_description="Get a single blog post", response_model=BlogPost)
async def get_post(post_id: str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")
    
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

@router.put("/posts/{post_id}", response_description="Update a blog post", response_model=BlogPost)
async def update_post(post_id: str, post: BlogPost):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    update_result = await db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": jsonable_encoder(post)})
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post = await db.posts.find_one({"_id": ObjectId(post_id)})
    return updated_post

@router.delete("/posts/{post_id}", response_description="Delete a blog post")
async def delete_post(post_id: str):
    if not ObjectId.is_valid(post_id):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    delete_result = await db.posts.delete_one({"_id": ObjectId(post_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Post deleted successfully"}