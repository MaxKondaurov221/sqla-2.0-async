from fastapi import FastAPI, Depends
import uvicorn
from views.calc import router as router_calc
from config import settings
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(router_calc, prefix="/calc")
app.add_middleware(
    CORSMiddleware,
        allow_origins=settings.cors.allow_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
)
@app.get("/hello")
def hello_by_qs(name:str = "World"):
    return {"message": f"Hello! {name}"}

@app.get("/hello/{name}")
def hello_by_path(name:str):
    return {"message": f"Hello {name}"}


@app.get("/hi")
@app.get("/hi/{name}")
def hello_by_path(name:str = 'World'):
    return {"message": f"Hi {name}"}
@app.post("/hello/{name}")
def hello_by_path(name:str = 'World'):
    return {"message": f"Hello {name}"}




if __name__ == '__main__':
    uvicorn.run('main:app',
                host = settings.host,
                port = settings.port,
                reload=settings.reload
                )
