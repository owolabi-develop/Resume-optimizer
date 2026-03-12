from fastapi import FastAPI

app = FastAPI(title="Resume Optimizer",
              summary="Advance resume optimization system for ATS (Application Tracking system)")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}