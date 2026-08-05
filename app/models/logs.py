from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProcessingLog(BaseModel):
    file_name: str

    stage: str

    timestamp: datetime

    duration_ms: int

    model: str

    prompt_version: str

    success: bool

    retries: int = 0

    error_message: Optional[str] = None