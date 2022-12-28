from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def raiz():
    return {"msg":"Fast API"}


if __name__ == "__main__":
    import uvicorn
    #import gunicorn

    #gunicorn main:app -W 4 -k uvicorn.workers.UvicornWorker
    uvicorn.run("main:app", host="127.0.0.1", port=8000, 
                log_level="info", reload=True)