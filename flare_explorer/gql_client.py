from dataclasses import dataclass

import requests
from pydantic import BaseModel

from flare_explorer.exceptions import (
    FlareExplorerNoneBadResponseCode,
    FlareExplorerQueryError,
)

BASE_URL = "https://flare-explorer.flare.network/graphiql"


class PageInfo(BaseModel):
    endCursor: str
    hasNextPage: bool
    hasPreviousPage: bool
    startCursor: str


@dataclass
class Client:
    base_url: str = BASE_URL

    def query(self, query: str) -> dict | None:
        response = requests.post(url=self.base_url, json={"query": query})
        response.raise_for_status()
        if response.status_code >= 300:
            raise FlareExplorerNoneBadResponseCode(
                f"Status code of {response.status_code} returned"
            )
        if query_errors := response.json().get("errors"):
            raise FlareExplorerQueryError([i["message"] for i in query_errors])
        if not response.json().get("data"):
            raise FlareExplorerQueryError("Data field in response is empty")
        return response.json()["data"]
