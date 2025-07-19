from server import app
from auth.api import auth_router
from user.api import user_router
from wflow.api import wflow_router

app.include_router(wflow_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/test")
async def root():
    return {"message": "hahahahahahahahahahahahahahahahahahahahaha!!!!"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8001)
