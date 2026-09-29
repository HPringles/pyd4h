from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


class ResourceType(StrEnum):
    MEMBER = "Member"
    MEMBER_QUALIFICATION = "MemberQualification"
    MEMBER_QUALIFICATION_AWARD = "MemberQualificationAward"
    CUSTOM_MEMBER_STATUS = "CustomMemberStatus"
    RETIRED_REASON = "RetiredReason"
    ROLE = "Role"
    TEAM = "Team"
    LOCATION_BOOKMARK = "LocationBookmark"
    EQUIPMENT_LOCATION = "EquipmentLocation"
    ORGANISATION = "Organisation"
    MEMBER_GROUP = "MemberGroup"
    MEMBER_GROUP_MEMBERSHIP = "MemberGroupMembership"
    ACTIVITY_ATTENDANCE="ActivityAttendance"
    INCIDENT = "Incident"
    EVENT = "Event"
    EXERCISE = "Exercise"
    TAG = "Tag"

@dataclass
class ResourceLink:
    id: Optional[int]
    resourceType: ResourceType
        

@dataclass
class Location:
    type: str
    coordinates: tuple

@dataclass
class Address:
    postcode: Optional[str]
    region: Optional[str]
    street: Optional[str]
    town: Optional[str]
    country: Optional[str]
