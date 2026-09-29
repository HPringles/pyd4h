from dataclasses import dataclass, field
from typing import Optional, Union
from enum import StrEnum
from datetime import datetime
import msgspec

from d4h.resources.resources import Address, Location, ResourceLink, ResourceType

class LocationBookmark(msgspec.Struct, kw_only=True):
    id: int
    title: str | None
    address: Address | None
    location: Location | None
    owner: ResourceLink | None
    parent: ResourceLink | None
    resourceType: ResourceType
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    archivedAt: Optional[datetime]