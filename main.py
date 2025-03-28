from fastapi import FastAPI
from src.routers import router


app = FastAPI(
    title="Yandex-auth uploader FastAPI",
    description="API для загрузки и удаления изображений",
    version="1.0.0",
)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
