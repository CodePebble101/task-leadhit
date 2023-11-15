from pydantic import BaseModel


class BasicResponse(BaseModel):
    status: str
    data: dict = None
    details: str = None



