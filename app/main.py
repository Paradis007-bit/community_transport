from fastapi import FastAPI
from .routes.transport_routes import router as transport_router

def create_app():
    app = FastAPI(title="Community Transport API")
    app.include_router(transport_router)
    @app.get("/")
    def root():
        return {"message": "Community Transport API is running"}
    return app

app = create_app()
