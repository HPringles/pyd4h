from dataclasses import dataclass, field
from typing import Optional, Union
from enum import StrEnum
from datetime import datetime
import msgspec

from d4h.resources.resources import Location, ResourceLink, ResourceType

class MemberQualification(msgspec.Struct, kw_only=True):
    id: int
    owner: ResourceLink

    title: str
    description: Optional[str]
    
    cost: Optional[int | str]
    expiredCost: Optional[int | str]
    
    deprecatedBundle: Optional[str]
    expiresMonthsDefault: Optional[int]

    reminderDays: Optional[int]
    
    createdAt: datetime
    updatedAt: datetime

    resourceType: ResourceType

class MemberQualificationAward(msgspec.Struct, kw_only=True):
    id: int
    member: ResourceLink
    qualification: ResourceLink

    startsAt: datetime
    endsAt: Optional[datetime]

    owner: ResourceLink

    createdAt: datetime
    updatedAt: datetime

    resourceType: ResourceType
