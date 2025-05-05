from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_message: str
    history: Optional[List[dict]] = []
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 150
    model_name: str = "Llama-3-ELYZA-JP-8B-q4_k_m.gguf"

class ChatResponse(BaseModel):
    bot_message: str
    history: List[dict]