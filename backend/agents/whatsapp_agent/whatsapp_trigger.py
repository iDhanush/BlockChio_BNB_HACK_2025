from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse

echo_route = APIRouter(prefix="/whatsapp")

@echo_route.post("/trigger")
async def receive_whatsapp(
    Body: str = Form(...),
    From: str = Form(...)
):
    print(f"Message from {From}: {Body}")
    return PlainTextResponse("OK")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
