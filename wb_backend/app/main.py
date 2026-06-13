from fastapi import FastAPI

from wb_backend.app.db import init_db


app = FastAPI(
    title="Workbench"
)


init_db()


@app.get("/")
def root():
    return {
        "status": "Workbench API Running"
    }