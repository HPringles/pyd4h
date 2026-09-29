from dataclasses import dataclass, field
from typing import Optional, Union
from enum import StrEnum
from datetime import datetime
import msgspec

from d4h.resources.resources import Location, ResourceLink, ResourceType


class Duty(StrEnum):
    ON = "ON"
    OFF = "OFF"

@dataclass
class EmailAddress:
    value: Optional[str]
    verified: Optional[bool] = None

@dataclass
class TelephoneNumber:
    phone: Optional[str]
    verified: Optional[bool] = None

@dataclass
class EmergencyContact:
    name: Optional[str]
    primaryPhone: Optional[str]
    secondaryPhone: Optional[str]
    relation: Optional[str]

class MemberStatus(StrEnum):
    OPERATIONAL = "OPERATIONAL"
    NON_OPERATIONAL = "NON_OPERATIONAL"
    RETIRED = "RETIRED"
    OBSERVER = "OBSERVER"


# @dataclass
class Member(msgspec.Struct, kw_only=True):
    alertActivityApproval: Optional[bool] = None
    alertAllQualifications: Optional[bool] = None
    alertGear: Optional[bool] = None
    alertQualifications:Optional[bool] = None
    chatAutosubscribe: Optional[bool] = None
    chatDailyDigest: Optional[bool] = None
    costPerHour: Optional[int] = None
    costPerUse: Optional[int] = None
    countReportingEvent: Optional[int] = None
    countReportingExcercise: Optional[int] = None
    countReportingIncident: Optional[int] = None
    countRollingHours: Optional[int] = None
    countRollingHoursEvent: Optional[int] = None
    countRollingHoursExercise: Optional[int] = None
    countRollingHoursIncident: Optional[int] = None

    percReportingEvent: Optional[int] = None
    percReportingIncident: Optional[int] = None
    percReportingExercise: Optional[int] = None

    permission: Optional[int] = None
    
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    deletedAt: Optional[datetime]
    
    startsAt: Optional[datetime]
    endsAt: Optional[datetime] # Think this is duty end time, or maybe rolling period end time?
    
    defaultDuty: Duty

    defaultEquipmentLocation: ResourceLink
    
    deprecatedAddress: Optional[str]
    
    email: EmailAddress
    mobile: TelephoneNumber

    primaryEmergencyContact: EmergencyContact
    secondaryEmergencyContact: EmergencyContact

    icalSecret: Optional[str]

    id: int
    idTag: Optional[str]

    lastLogin: Optional[datetime]

    location: Location
    locationBookmark: ResourceLink

    ref: str
    name: str
    position: str
    notes: Optional[str] = None
    status: MemberStatus
    
    
    pager: dict
    retiredReason: ResourceLink

    role: ResourceLink

    signedTandC: Optional[datetime]

    customStatus: ResourceLink

    teamAgreementSigned: Optional[str]
    owner: ResourceLink

    weeklyDayOfWeek: Optional[int] = None
    weeklyDayOfWeekUtc: Optional[int] = None
    weeklyHourOfDay: Optional[int] = None
    weeklyHourOfDayUtc: Optional[int] = None
    weeklyMail: Optional[bool] = None

    work: TelephoneNumber

    resourceType: ResourceType

class Member_EssentialOnly(msgspec.Struct, kw_only=True):
    email: EmailAddress

    id: int
    idTag: Optional[str]

    ref: str
    name: str
    position: str
    notes: Optional[str] = None
    status: MemberStatus

    role: ResourceLink

    owner: ResourceLink

    resourceType: ResourceType
