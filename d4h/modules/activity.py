from datetime import datetime, timezone
from enum import StrEnum

from d4h.exception import D4HException
from d4h.resources.location_bookmark import LocationBookmark
from d4h.resources.tag import Tag
import msgspec
from d4h.module import D4HModule
from d4h.resources.activity import Activity
import logging


class ActivityModule(D4HModule):
    def get(self, activity_type: str, activity_id: int) -> Activity:
        res = self._get(f"{activity_type}s/{activity_id}")

        return msgspec.convert(res, Activity)

    def post(
        self,
        activity_type: str,
        # reference: str = None,
        reference_description: str = None,
        description: str | None = None,
        plan: str | None = None,
        tracking_number: str = None,
        shared: bool = None,
        full_team: bool = None,
        address: dict | None = {},
        location: dict | None = {},
        location_bookmark_id: int = None,
        starts_at: datetime | str = None,
        ends_at: datetime | str = None,
        custom_field_values: list[dict] | None = [],
    ) -> dict[any, any]:

        if activity_type not in ["exercise", "event", "incident"]:
            raise ValueError("Invalid activity type")

        if isinstance(starts_at, datetime):
            starts_at = starts_at.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        if isinstance(ends_at, datetime):
            ends_at = ends_at.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        reference = self.increment_autoid(activity_type)

        if location_bookmark_id and not location:
            expanded_location_bookmark: LocationBookmark = self.get_location_bookmark(location_bookmark_id)
            address = expanded_location_bookmark['address']
            coords = expanded_location_bookmark['location']['coordinates']
            location = {"latitude": coords[1], "longitude": coords[0]}

        if not location:
            raise D4HException("Either location or location_bookmark_id must be provided.")

        params = {
            "reference": reference,
            "referenceDescription": reference_description,
            "description": description,
            "plan": plan,
            "trackingNumber": tracking_number,
            "shared": shared,
            "fullTeam": full_team,
            "address": address,
            "location": location,
            "locationBookmarkId": location_bookmark_id,
            "startsAt": starts_at,
            "endsAt": ends_at,
            "customFieldValues": custom_field_values,
        }

        return msgspec.convert(self._post(f"{activity_type}s", json=params), Activity)

    def set_activity_tags(self, activity_type: str, activity_id: int, tags: list[int]) -> dict[any, any]:
        if self._connection.context.value != "team":
            raise D4HException("Setting activity tags is only available in team context.")
        return self._post(f"{activity_type}s/{activity_id}/tags", json={"tagIds": tags})

    def increment_autoid(self, activity_type: str) -> dict[any, any]:
        if self._connection.context.value != "team":
            raise D4HException("Incrementing autoid is only available in team context.")
        if activity_type not in ["exercise", "event", "incident"]:
            raise ValueError("Invalid activity type")
        return self._post(f"{activity_type}s/reference/increment")['reference']
    
    def get_location_bookmark(self, bookmark_id: int) -> LocationBookmark:
        res = self._get(f"location-bookmarks/{bookmark_id}")
        return res

    def get_all_tags(self) -> list[Tag]:
        res = self._get("tags")
        return [msgspec.convert(r, Tag) for r in res]