from pydantic import BaseModel

class UrlRequest(BaseModel):
    url : str

class ChatRequest(BaseModel):
    question : str

class ChatResponse(BaseModel):
    answer : str
