from abc import ABC, abstractmethod
from functools import cached_property

from gql import Client as GqlClient, gql
from gql.transport import Transport
from gql.transport.requests import RequestsHTTPTransport
from pydantic import BaseModel

from flare_explorer.exceptions import (
    FlareExplorerQueryError,
)

API_URL = "https://flare-explorer.flare.network/graphiql"

class PageInfo(BaseModel):
    endCursor: str | None
    hasNextPage: bool
    hasPreviousPage: bool
    startCursor: str | None


def generate_after_pagination_query_line(previous_cursor: str | None) -> str:
    return f'after: "{previous_cursor}"' if previous_cursor else ""


class BaseClient(ABC):

    @property
    @abstractmethod
    def _transport(self) -> Transport:
        """Over-ridden transport for each child class"""

    @cached_property
    def _client(self) -> GqlClient:
        return GqlClient(transport=self._transport, execute_timeout=None)


class Client(BaseClient):
    @cached_property
    def _transport(self) -> RequestsHTTPTransport:
        return RequestsHTTPTransport(url=API_URL, verify=True, retries=3)

    def query(self, query: str) -> dict | None:
        """
        Query flares graphql api
        Args:
            query: query str

        Returns:
            contents of the data key returned from flare
        """
        response = self._client.execute(gql(query))
        if not response:
            raise FlareExplorerQueryError("Data field in response is empty")
        return response
