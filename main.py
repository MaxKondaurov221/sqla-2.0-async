from fastapi import FastAPI
import uvicorn
from views.calc import router as router_calc
from views.users.views import router as router_users

from config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router_calc, prefix="/calc")
app.include_router(router_users, prefix="/users")

app.add_middleware(
    CORSMiddleware,
        allow_origins=settings.cors.allow_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
)


if __name__ == '__main__':
    uvicorn.run('main:app',
                host = settings.host,
                port = settings.port,
                reload=settings.reload
                )
