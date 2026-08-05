from pydantic import BaseModel

class Experience(BaseModel):
    company:str
    experience:str
    years:int
    start_date:str
    end_date:str
    