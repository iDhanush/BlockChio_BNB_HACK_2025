import traceback
from globar_vars import Var
from database import DataBase
from fastapi import FastAPI, Request
from pydantic import ValidationError
from responses import StandardException
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


# ON STARTUP FUNCTION
@asynccontextmanager
async def lifespan(_fastapi: FastAPI):
    Var.db = DataBase()
    yield


# Shutdown event
async def shutdown_event():
    print("Shutting down...")


LIMITED_PATHS = ["/v1/chat/send-message"]
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(_request: Request, exc: ValidationError):
    error = str(exc.errors())
    print(error)
    raise StandardException(
        status_code=422,
        details=error,
        message=error
    )


@app.exception_handler(StandardException)
async def standard_exception_handler(_request: Request, exc: StandardException):
    if Var.TEST_MODE:
        traceback.print_exc()
        print('no worries already handled error ☝️')
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "details": exc.details,
            "message": exc.message
        }
    )
