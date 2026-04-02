from typing import Literal

from pydantic import BaseModel, Field

TrustLabel = Literal["trusted", "blocked"]

class SourceDocument(BaseModel):
    source_id: str = Field(..., min_length = 1)
    title: str = Field(..., min_length = 1)
    source_url: str = Field(..., min_length = 1)
    source_type: str = Field(..., min_length = 1)
    trust_label: TrustLabel
    content: str = Field(..., min_length = 1)

