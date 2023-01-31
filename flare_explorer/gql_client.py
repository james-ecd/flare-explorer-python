from dataclasses import dataclass
from functools import cached_property

from gql import Client as GqlClient, gql
from gql.transport.requests import RequestsHTTPTransport
from pydantic import BaseModel

from flare_explorer.exceptions import (
    FlareExplorerQueryError,
)

BASE_URL = "https://flare-explorer.flare.network/graphiql"


class PageInfo(BaseModel):
    endCursor: str | None
    hasNextPage: bool
    hasPreviousPage: bool
    startCursor: str | None


def generate_after_pagination_query_line(previous_cursor: str | None) -> str:
    return f'after: "{previous_cursor}"' if previous_cursor else ""


@dataclass
class Client:
    base_url: str = BASE_URL

    @cached_property
    def _transport(self) -> RequestsHTTPTransport:
        return RequestsHTTPTransport(url=self.base_url, verify=True, retries=3)

    @cached_property
    def _client(self) -> GqlClient:
        return GqlClient(transport=self._transport)

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
