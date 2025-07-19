from pydantic import BaseModel, Field


class ImagePrompt(BaseModel):
    prompt: str = Field(..., description="The prompt to generate the image")

class BlockchainPrompt(BaseModel):
    query: str = Field(..., description="The prompt for the blockchain_agent agent")
