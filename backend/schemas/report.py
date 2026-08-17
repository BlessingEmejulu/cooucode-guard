from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class ReportCreate(BaseModel):
    scan_id: int
    report_format: Optional[str] = "HTML"

class ReportResponse(BaseModel):
    id: int
    scan_id: int
    title: str
    file_path: Optional[str] = None
    report_format: str
    summary_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
