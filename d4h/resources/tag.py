from dataclasses import dataclass, field
from typing import Optional, Union
from enum import StrEnum
from datetime import datetime
import msgspec

from d4h.resources.resources import Location, ResourceLink, ResourceType

class Tag(msgspec.Struct, kw_only=True):
    id: int
    title: str
    notes: Optional[str]
    resourceType: ResourceType
    owner: ResourceLink
    updatedAt: Optional[datetime]
    createdAt: Optional[datetime]