from fastapi import FastAPI

app = FastAPI()


@app.get('/test/a={a}/b={b}')
def cal(a: int = None, b: int = None):
    c = a + b
    return {"res": c}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8080,
                workers=1)
