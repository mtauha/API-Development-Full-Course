from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()
my_posts = [{"title":"title of post 1", "content":"title of post 1", "id":1},
            {"title":"Favourite Places", "content":"Istanbul", "id":2}]



class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message":"Welcome to my API"}

@app.get("/posts")
async def get_post():
    return {"data":my_posts}

@app.post("/posts")
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000)
    #my_posts.append(post_dict)
    return {"data":my_posts}


#* NOTES:

# @app.get("/") -> Decorator
# 'async' -> ASynchronous keyword used for methods that invloves time factor like APIs and stuf (It is not necessary code will work without it just fine).