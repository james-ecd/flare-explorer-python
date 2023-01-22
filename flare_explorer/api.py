from dataclasses import dataclass

import requests


@dataclass
class Api:
    base_url: str = "https://flare-explorer.flare.network/graphiql"

    def make_request(self, query: str) -> list | dict | None:
        response = requests.post(url=self.base_url, json={"query": query})
        response.raise_for_status()
        return response.json()
