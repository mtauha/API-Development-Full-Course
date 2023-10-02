from fastapi import FastAPI

app = FastAPI()


@app.get(url="/")
async def root():
    return {"message":"Hello World!"}

@app.get(url="/posts")
async def get_post():
    return {"data":"This is your posts"}

#* NOTES:

# @app.get("/") -> Decorator
# 'async' -> ASynchronous keyword used for methods that invloves time factor like APIs and stuf (It is not necessary code will work without it just fine).