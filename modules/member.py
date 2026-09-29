from datetime import datetime
from enum import StrEnum

import msgspec
from d4h.module import D4HModule
from d4h.resources.member import Member, Member_EssentialOnly
import logging

class MemberModule(D4HModule):

    def get (self, member_id: int, full_info: bool = False) -> Member | Member_EssentialOnly:
        res = self._get(f"members/{member_id}")
        # print(res)
        # return from_dict(Member, res, config=Config(type_hooks={datetime: datetime.fromisoformat, StrEnum: StrEnum}))
        return msgspec.convert(res, Member_EssentialOnly if not full_info else Member)

    def get_by_name(self, name: str = None, full_info: bool = False) -> Member | Member_EssentialOnly:
        res = self._get("members", params={"name": name, "status": ["NON_OPERATIONAL", "OBSERVER", "OPERATIONAL", "RETIRED"]})
        print(res)
        if isinstance(res, list):
            res = res[0]
        else:
            return None
        return msgspec.convert(res, Member_EssentialOnly if not full_info else Member)

    def get_many(self,
                 member_ids: list[int] | int = None,
                 status: str = None,
                 size: int = 250,
                 page: int = 0,
                 full_info: bool = False
                 ) -> list[Member | Member_EssentialOnly]:
        params = {"status": status,
                  "size": size,
                  "page": page,
                  "id": member_ids}

        params = {k: v for k, v in params.items() if v}
        res = self._get("members", params=params)
        # logging.debug("res: ", res)
        ret = []
        # return [msgspec.convert(
        #     r, Member_EssentialOnly if not full_info else Member) for r in res]
        
        for r in res:
            try:
                ret.append(msgspec.convert(r, Member_EssentialOnly if not full_info else Member))
            except Exception as e:
                logging.error(f"Error converting member {r['id']}: {e}")
        
        return ret
