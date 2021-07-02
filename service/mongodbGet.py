import pymongo
from fastapi import FastAPI

app = FastAPI()


@app.get('/test')
def cal():
    mongoClient = pymongo.MongoClient('m')

    myDb = mongoClient['dqj_jinshidata']
    myCol = myDb['news']
    dataList = []
    for data in myCol.find():
        dataList.append(data)
    return dataList


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8080,
                workers=1)
