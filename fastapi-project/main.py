from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello world 🚀"}


@app.get("/user/{name}")
def read_item(name: str):
    return {"message": f"Hello {name}, welcome to FastAPI"}
