"""Qualification class for use as a module in D4Hconnection."""


from datetime import datetime, timezone
from enum import StrEnum

import msgspec
from d4h.module import D4HModule

from d4h.resources.member_qualification import MemberQualification, MemberQualificationAward


class MemberQualificationModule(D4HModule):
    def get(self, qualification_id: int) -> MemberQualification:
        return msgspec.convert(self._get(f"member-qualifications/{qualification_id}"), MemberQualification)

    def get_many(self,
                 title: str = "",
                 page_size: int = 250,
                 page: int = 0
                 ) -> list[MemberQualification]:
        params = {
            "title": title,
            "size": page_size,
            "page": page
        }

        params = {k: v for k, v in params.items() if v}

        res = self._get("member-qualifications", params=params)
        return [
            msgspec.convert(r, MemberQualification) for r in res
        ]

    def get_qualified_members(
            self,
            qualification_id: int,
            in_date_only: bool = True,
            page_size: int = 250,
            page: int = None,

    ) -> list[MemberQualificationAward]:
        params = {
            "qualification_id": qualification_id,
            "size": page_size,
            "page": page
        }

        params = {k: v for k, v in params.items() if v}

        res = self._get("member-qualification-awards", params=params)

        results = []

        if in_date_only:
            results = [
                r for r in res if not r.get('endsAt', None) or datetime.fromisoformat(r.get('endsAt')) >= datetime.now().astimezone()
            ]
        else:
            results = res

        return [[msgspec.convert(r, MemberQualificationAward) for r in results]]

    # def get_member_qualifications(
    #         self,
    #         member_id: int,
    #         in_date_only: bool = True,
    #         page_size: int = 250,
    #         page: int = None,

    # ) -> list[dict[str, any]]:
    #     params = {
    #         "member_id": member_id,
    #         "size": page_size,
    #         "page": page
    #     }

    #     params = {k: v for k, v in params.items() if v}

    #     res = self._get("member-qualification-awards", params=params)

    #     results = []

    #     if in_date_only:
    #         results = [
    #             r for r in res if not r.get('endsAt', None) or datetime.fromisoformat(r.get('endsAt')) >= datetime.now().astimezone()
    #         ]
    #     else:
    #         results = res

    #     return [msgspec.convert(r, MemberQualificationAward) for r in results]

    def get_member_qualifications(
            self,
            member_id: int,
            in_date_only: bool = True,
            page_size: int = 250,
            page: int = None,
            get_all_pages: bool = False

    ) -> list[dict[str, any]]:
        params = {
            "member_id": member_id,
            "size": page_size,
            "page": page
        }

        res = []

        params = {k: v for k, v in params.items() if v}

        if get_all_pages:
            page = 0
            all_results = []
            while True:
                params["page"] = page
                res = self._get("member-qualification-awards", params=params)
                print(len(res))
                if isinstance(res, dict) or len(res) == 0:
                    break
                all_results += res
                page += 1
            res = all_results
        else:

            res = self._get("member-qualification-awards", params=params)

        results = []

        if in_date_only:
            results = [
                r for r in res if not r.get('endsAt', None) or datetime.fromisoformat(r.get('endsAt')) >= datetime.now().astimezone()
            ]
        else:
            results = res

        return [msgspec.convert(r, MemberQualificationAward) for r in results]

    def post_member_qualification(
            self,
            member_id: int,
            qualification_id: int,
            start_date: datetime | str,
            end_date: datetime | str = "null"
    ) -> dict[any, any]:
        if isinstance(start_date, datetime):
            start_date = start_date.astimezone(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        if isinstance(end_date, datetime):
            end_date = end_date.astimezone(
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        return self._post(
            "member-qualification-awards",
            json={
                "memberId": member_id,
                "qualificationId": qualification_id,
                "startsAt": start_date,
                "endsAt": end_date,
            }
        )
    
    def delete_member_qualification(
        self,
        qualification_id:int) -> dict[any, any]:
        return self._del(f"member-qualifications/{qualification_id}")
