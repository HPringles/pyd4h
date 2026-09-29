from typing import TYPE_CHECKING

# import msgspec
from d4h.exception import D4HException
from d4h.resources.location_bookmark import LocationBookmark
from d4h.resources.tag import Tag


if TYPE_CHECKING:
    from d4h.connection import D4HConnection


class D4HModule:
    _connection = "D4HConnection"

    def __init__(self, connection: "D4HConnection"):
        self._connection = connection

    def _get(self, endpoint: str, ignore_context: bool = False, **kwargs) -> list[dict[any, any]] | dict[any, any]:
        """Get data from an endpoint, returning the json data field.

        Args:
            endpoint (str): the endpoint (after the /team/) to get from.

        Raises:
            D4HException: If there is an issue with the D4H request.
                (i.e) a non-OK HTTP response.

        Returns:
            Dict[Any, Any]: the 'data' field of the JSON response.
        """

        res = self._connection.get(
            endpoint, ignore_context=ignore_context, **kwargs)
        if res.ok:
            if data := res.json().get("results"):
                if not isinstance(data, list):
                    data = [data]
                return data
            else:
                return res.json()
        else:
            raise D4HException(
                f"Non-Zero Error Code: {res.status_code}, {endpoint}, {res.reason}\
                    , {res.json()}", status_code=res.status_code,
            )

    def _post(self, endpoint: str, ignore_context: bool = False, **kwargs) -> dict[any, any]:
        """Make a post request to an endpoint, on a specific instence.

        Args:
            endpoint (str): endpoint to query (after /team/)
            ignore_context (bool, optional): ignore the context part of  the URL, details to false.
            **kwargs: keword arugmentts for requests.post

        Raises:
            D4HException

        Returns:
            Dict[Any, Any]: Result obtained from the query.
        """
        res = self._connection.post(
            endpoint, ignore_context=ignore_context, **kwargs)
        if res.ok:
            return res.json()
        else:
            print(res.json())
            raise D4HException(f"error: {res.status_code}: {res.reason}")

    def _del(self, endpoint: str, ignore_context: bool = False, **kwargs) -> dict[any, any]:
        res = self._connection.delete(
            endpoint, ignore_context=ignore_context, **kwargs)
        if res.ok:
            return res.json()
        else:
            print(res.json())
            raise D4HException(f"error: {res.status_code}: {res.reason}")
