from pydantic import BaseModel, Field
from typing import Optional

class AuditRequest(BaseModel):
    texto: str = Field(..., min_length=1)
    origem: Optional[str] = Field(default=None)

class AuditResponse(BaseModel):
    id: Optional[int] = None
    score_confianca: float
    folgas_detectadas: list[str]
    parecer: str
    avaliacao_ia: Optional[str] = None
    origem: str
    data_hora: Optional[str] = None
