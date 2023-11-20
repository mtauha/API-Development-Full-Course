from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
import subprocess as sb


host = os.environ.get("host")
database = os.environ.get("database")
user = os.environ.get("user")
password = os.environ.get("password")

app = FastAPI()
my_posts = [{"title":"title of post 1", "content":"title of post 1", "id":1},
            {"title":"Favourite Places", "content":"Istanbul", "id":2}]

condition = False
while condition == False:
    try:
        connection = psycopg2.connect(host=host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Connected Successfully!")
        condition = True

    except Exception as error:
        print("Connection Failed")
        print("Error: ", error)
        time.sleep(2)

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


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
    cursor.execute("""SELECT * FROM "Posts" """)
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute("""INSERT INTO "Posts"(title, content) VALUES(%s,%s,%s) RETURNING * """,(post.title, post.content, post.published))

    post = cursor.fetchone()
    connection.commit()

    return {"data": post}


@app.get("/posts/latest")
async def get_latest_post():
    cursor.execute("""SELECT * FROM "Posts" ORDER BY id DESC LIMIT 1""")
    post = cursor.fetchone()
    return {"post detail": post}


@app.get("/posts/{id}")
async def get_post(id: int):

    cursor.execute("""SELECT * FROM "Posts" WHERE id = %s""", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    
    return {"post detail": post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM "Posts" WHERE id = %s RETURNING *""", (str(id)))
    post = cursor.fetchall()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")

    connection.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE "Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (str(post.title), post.content, post.published, str(id)))
    index = find_index_post(id=id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")

    post_dict = post.dict()
    post_dict['id'] = id

    my_posts[index] = post_dict

    return {"update": post_dict}


#* NOTES:

# @app.get("/") -> Decorator
# 'async' -> ASynchronous keyword used for methods that invloves time factor like APIs and stuf (It is not necessary code will work without it just fine).

# Resume Video From  4:24:55