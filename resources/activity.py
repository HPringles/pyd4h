from dataclasses import dataclass, field
from typing import Optional, Union
from enum import StrEnum
from datetime import datetime
import msgspec

from d4h.resources.resources import Location, ResourceLink, ResourceType, Address


@dataclass
class Weather:
    symbol: Optional[str]
    symbolDate: Optional[datetime]
    temperature: Optional[float]


@dataclass
class Location:
    type: Optional[str]
    coordinates = Optional[tuple]


class Activity(msgspec.Struct, kw_only=True):
    id: int
    reference: str
    referenceDescription: str

    description: Optional[str]
    plan: Optional[str]

    owner: ResourceLink
    locationBookmark: ResourceLink
    weather: Optional[Weather]
    address: Optional[Address]
    location: Optional[Location]
    resourceType: ResourceType

    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    deletedAt: Optional[datetime]
    createdOrPublishedAt: Optional[datetime]

    startsAt: Optional[datetime]
    endsAt: Optional[datetime]
    night: Optional[bool]

    bearing: Optional[int]
    coordinator: None
    distance: Optional[int]

    shared: Optional[bool]
    published: Optional[bool]
    fullTeam: Optional[bool]

    countAttendance: Optional[int]
    countGuests: Optional[int]
    percAttendance: Optional[int]
    selfCoordinator: Optional[bool]
    trackingNumber: Optional[str]

    tags: Optional[list[ResourceLink]]
    cusomFieldValues = Optional[list[dict]]
