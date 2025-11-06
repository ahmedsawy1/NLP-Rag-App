from fastapi import FastAPI

app = FastAPI()

print("Hello, World!")

@app.get("/")
def read_root():
    return {"message": "Hello, World! From Fast API ^_^"}