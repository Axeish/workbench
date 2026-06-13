from fastapi import FastAPI

from wb_backend.app.db import init_db


app = FastAPI(
    title="Workbench"
)

app.include_router(artwork_router)
init_db()


@app.get("/")
def root():
    return {
        "status": "Workbench API Running"
    }