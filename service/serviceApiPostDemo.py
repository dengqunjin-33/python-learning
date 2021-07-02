from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    a: int = None
    b: int = None


@app.post('/test1')
def cal():
    return {"message": "傻乎乎的"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8080,
                workers=1)
