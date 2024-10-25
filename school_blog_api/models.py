from pydantic import BaseModel, Field
from typing import Optional

class BlogPost(BaseModel):
    title: str = Field(..., example="My First Blog Post")
    content: str = Field(..., example="This is the content of the blog post.")
    author: str = Field(..., example="Author Name")
    published: Optional[bool] = Field(default=False)