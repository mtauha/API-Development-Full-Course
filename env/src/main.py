from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()
my_posts = [{"title":"title of post 1", "content":"title of post 1", "id":1},
            {"title":"Favourite Places", "content":"Istanbul", "id":2}]



def find_id(id):
    for post in my_posts:
        if post['id'] == id:
            return post


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message":"Welcome to my API"}

@app.get("/posts")
async def get_posts():
    return {"data":my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000)
    #my_posts.append(post_dict)
    return {"data":my_posts}


@app.get("/posts/latest")
def get_latest_post():
    return {"post detail": my_posts[len(my_posts) - 1]}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_id(id=id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"status Code":response.status_code}
    print(post)
    return {"post detail": post}

#* NOTES:

# @app.get("/") -> Decorator
# 'async' -> ASynchronous keyword used for methods that invloves time factor like APIs and stuf (It is not necessary code will work without it just fine).