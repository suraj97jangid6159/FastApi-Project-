
from fastapi import FastAPI

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/") # decorator
def read_root():
    return {"Name": "Suraj Jangid",
            "Position":"Backend Development",
            "Tech":"Python stack"
            }