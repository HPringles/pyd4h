from dataclasses import dataclass, field
from typing import Optional, Union
from enum import StrEnum
from datetime import datetime
import msgspec

from d4h.resources.resources import Location, ResourceLink, ResourceType

class AttendanceStatus(StrEnum):
    REQUESTED = "REQUESTED"
    ATTENDING = "ATTENDING"
    ABSENT = "ABSENT"

class Attendance(msgspec.Struct, kw_only=True):
    id: int
    
    activity: ResourceLink
    member: ResourceLink
    owner: ResourceLink

    status: AttendanceStatus

    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

    startsAt: Optional[datetime]
    duration: Optional[int]
    endsAt: Optional[datetime]

    role: Optional[ResourceLink]

    resourceType: ResourceType

