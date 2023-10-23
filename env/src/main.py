from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message":"Welcome to my API"}

@app.get("/posts")
async def get_post():
    return {"data":"This is your posts"}

@app.post("/creatingposts")
async def create_posts(post: Post):
    print(post)
    return {"data":"new_post"}

#* NOTES:

# @app.get("/") -> Decorator
# 'async' -> ASynchronous keyword used for methods that invloves time factor like APIs and stuf (It is not necessary code will work without it just fine).