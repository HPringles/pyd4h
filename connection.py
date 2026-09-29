from typing import Callable
import requests
from enum import Enum
from logging import getLogger

from d4h.modules.activity import ActivityModule
from d4h.modules.group import MemberGroupModule
from d4h.modules.member import MemberModule
from d4h.modules.member_qualification import MemberQualificationModule
from d4h.modules.attendance import AttendanceModule
from d4h.exception import D4HException
from d4h.resources.resources import ResourceLink, ResourceType

logger = getLogger(__name__)

class Context(Enum):
    TEAM = "team"
    ORGANISATION = "organisation"

RESOURCE_TO_GET_REQUEST: dict[ResourceType, Callable["D4HConnection", ResourceLink]] = {
    ResourceType.MEMBER: lambda connection, resource: connection.member.get(resource.id),
    ResourceType.MEMBER_GROUP: lambda connection, resource: connection.group.get(resource.id),
    ResourceType.MEMBER_QUALIFICATION: lambda connection, resource: connection.qualification(resource.id)
}

class D4HConnection:
    name: str
    link_url: str
    access_token: str
    base_url: str = "https://api.team-manager.us.d4h.com/v3"
    context_url: str

    context: Context = Context.TEAM
    contextId: int

    # Connectors / Entities

    member: MemberModule
    member_qualification: MemberQualificationModule
    group: MemberGroupModule

    attendance: AttendanceModule
    activity: ActivityModule

    def __init__(self, name: str, access_token: str, context: str, contextId: int):
        self.name = name
        self.access_token = access_token

        self.context = context
        self.contextId = contextId

        self.context_url = f"{self.base_url}/{context.value}/{contextId}"

        connection_test = self.get('whoami', ignore_context=True)
        if connection_test.status_code != 200:
            raise D4HException(
                f"Unable to connect to D4H, status code: {connection_test.status_code}")
        else:
            logger.info("Connection to D4H API v3 Successful!")

        self._init_entities()

    def _init_entities(self):

        self.member = MemberModule(self)
        self.member_qualification = MemberQualificationModule(self)
        self.group = MemberGroupModule(self)
        self.attendance = AttendanceModule(self)
        self.activity = ActivityModule(self)

    def resolve_resource_link(self, resourceLink: ResourceLink):
        try:
            return RESOURCE_TO_GET_REQUEST[resourceLink.resourceType](self, resourceLink)
        except KeyError:
            raise D4HException(f"Cannot resolve link of Resource Type: {resourceLink.resourceType}. Unsupported by d4h package.")

    def get(self, endpoint: str, ignore_context=False, **kwargs) -> requests.Response:
        if kwargs.get("headers", None):
            kwargs["headers"]["Authorization"] = f"Bearer {self.access_token}"
        else:
            kwargs["headers"] = {
                "Authorization": f"Bearer {self.access_token}"}
        logger.debug(f"GET {self.base_url if ignore_context else self.context_url}{'/' if endpoint[0] != '/' else ''}{endpoint}",
                          )
        res = requests.get(
            f"{self.base_url if ignore_context else self.context_url}{'/' if endpoint[0] != '/' else ''}{endpoint}",
            **kwargs,
        )

        return res

    def post(self, endpoint: str, ignore_context=False, **kwargs) -> requests.Response:
        if kwargs.get("headers", None):
            kwargs["headers"]["Authorization"] = f"Bearer {self.access_token}"
        else:
            kwargs["headers"] = {
                "Authorization": f"Bearer {self.access_token}"}

        logger.debug(f"POST {self.base_url if ignore_context else self.context_url}{'/' if endpoint[0] != '/' else ''}{endpoint}",
                      )

        res = requests.post(
            f"{self.base_url if ignore_context else self.context_url}{'/' if endpoint[0] != '/' else ''}{endpoint}",
            **kwargs,
        )

        return res
    
    def delete(self, endpoint: str, ignore_context=False, **kwargs) -> requests.Response:
        if kwargs.get("headers", None):
            kwargs["headers"]["Authorization"] = f"Bearer {self.access_token}"
        else:
            kwargs["headers"] = {
                "Authorization": f"Bearer {self.access_token}"}

        logger.debug(f"DELETE {self.base_url if ignore_context else self.context_url}{'/' if endpoint[0] != '/' else ''}{endpoint}",
                      )

        res = requests.delete(
            f"{self.base_url if ignore_context else self.context_url}{'/' if endpoint[0] != '/' else ''}{endpoint}",
            **kwargs,
        )

        return res
