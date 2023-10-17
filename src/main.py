from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from core.config import app_settings
from api.v1.users import router_user
from api.v1.files import router_files
from api.v1.base import router_base


app = FastAPI(
    title=app_settings.app_title,
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    redoc_url=None
)

prefix = "/api/v1"

app.include_router(router_user, prefix=prefix, tags=["users"])
app.include_router(router_files, prefix=prefix, tags=['files'])
app.include_router(router_base, prefix=prefix, tags=['base'])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.project_host,
        port=app_settings.project_port
    )
