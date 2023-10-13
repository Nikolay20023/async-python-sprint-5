from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from core.config import app_settings
from api.v1.users import router_user


app = FastAPI(
    title=app_settings.app_title,
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    redoc_url=None
)

app.include_router(router_user, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=app_settings.project_host,
        port=app_settings.project_port
    )
