from pydantic import BaseModel
from typing import List


class ChunkMetadata(BaseModel):

    source: str
    page: int
    type: str
    section: str
    table_detected: bool


class ChunkSchema(BaseModel):

    content: str
    metadata: ChunkMetadata