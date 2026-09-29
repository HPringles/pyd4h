from datetime import datetime, timezone
from enum import StrEnum

from d4h.exception import D4HException
import msgspec
from d4h.module import D4HModule
from d4h.resources.attendance import Attendance, AttendanceStatus

import logging

class AttendanceModule(D4HModule):

    def get(self, attendance_id: int) -> Attendance:
        res = self._get(f"attendance/{attendance_id}")

        return msgspec.convert(res, Attendance)
    
    def get_many(
            self,
            attendance_ids: list[int] | int = None,
            activity_ids: list[int] | int = None,
            member_ids: list[int] | int= None,
            activity_resource_types: list[str] | str = None,
            deleted: bool = None,
            starts_after: datetime = None,
            starts_before: datetime = None,
            role_ids: list[int] | int = None,
            statuses: AttendanceStatus = None,
            order: str = None,
            sort: str = None,
            page: str = None,
            page_size: int = 250,
    ) -> list[Attendance]:
        
        params = {
            "id": attendance_ids,
            "activity_id": activity_ids,
            "member_id": member_ids,
            "activity_resource_type": activity_resource_types,
            "deleted": deleted,
            "starts_after": starts_after.astimezone(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') if starts_after else None,
            "starts_before": starts_before.astimezone(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') if starts_before else None,
            "role_id": role_ids,
            "status": statuses,
            "size": page_size,
            "page": page,
            "order": order,
            "sort": sort
        }

        params = {k:v for k,v in params.items() if v}

        res = self._get("attendance", params=params)
        if isinstance(res, list):
            return [
                msgspec.convert(r, Attendance) for r in res
            ]
        else: 
            return []

    def post(
            self,
            activity_id: int,
            member_id: int,
            role_id: int= None,
            starts_at: datetime | str = None,
            ends_at: datetime | str = None,
            status: AttendanceStatus = None
    ) -> Attendance:
        if self._connection.context.value != "team":
            raise D4HException("Adding attendance is only available in team context.")

        if isinstance(starts_at, datetime):
            starts_at = starts_at.astimezone(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        if isinstance(ends_at, datetime):
            ends_at = ends_at.astimezone(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        params = {
            "activityId": activity_id,
            "memberId": member_id,
            "roleId": role_id,
            "startsAt": starts_at,
            "endsAt": ends_at,
            "status": status
        }

        return msgspec.convert(self._post("attendance", json=params), Attendance)