from typing import Optional

from enum import StrEnum
from datetime import datetime
import msgspec

from d4h.resources.resources import ResourceLink, ResourceType

class MemberGroup(msgspec.Struct):
    id: int
    title: str
    deprecatedBundle: Optional[str]
    membershipResourceType: ResourceType
    owner: ResourceLink
    resourceType: ResourceType

    createdAt: datetime
    updatedAt: datetime

class MemberGroupMemberships(msgspec.Struct):
    id: int
    owner: ResourceLink
    group: ResourceLink
    member: ResourceLink

    resourceType: ResourceType
    createdAt: datetime
    updatedAt: datetime
    
