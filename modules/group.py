import msgspec

from d4h.module import D4HModule
from d4h.resources.group import MemberGroup, MemberGroupMemberships


class MemberGroupModule(D4HModule):

    def get(self, group_id: int) -> MemberGroup:
        res = self._get(f"member-groups/{group_id}")

        return msgspec.convert(res, MemberGroup)

    def get_many(self,
                 group_ids: list[int] | int = None,
                 title: str = None,
                 page_size: int = 250,
                 page: int = 0
                 ) -> list[MemberGroup]:

        params = {
            "id": group_ids,
            "title": title,
            "size": page_size,
            "page": page
        }

        res = self._get(f"member-groups",
                        params={k: v for k, v in params.items() if v})

        return [
            msgspec.convert(r, MemberGroup) for r in res
        ]

    def get_memberships(self,
                        group_ids: list[int] | int,
                        page_size: int = 250,
                        page: int = 0
        ) -> list[MemberGroupMemberships]:

        params = {
            "group_id": group_ids,
            "size": page_size,
            "page": page
        }

        res = self._get(f"member-group-memberships",
                        params={k: v for k, v in params.items() if v})

        return [
            msgspec.convert(r, MemberGroupMemberships) for r in res
        ]

    def get_groups_for_member(self,member_id: int) -> list[MemberGroupMemberships]:
        params = {
            "member_id": member_id
        }

        res = self._get(f"member-group-memberships",
                        params={k: v for k, v in params.items() if v})
        print(res)
        return [
            msgspec.convert(r, MemberGroupMemberships) for r in res
        ]
