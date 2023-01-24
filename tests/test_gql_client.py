import pytest
import requests_mock
from requests import HTTPError

from flare_explorer.gql_client import BASE_URL, Client
from flare_explorer.exceptions import (
    FlareExplorerNoneBadResponseCode,
    FlareExplorerQueryError,
)


class TestClient:
    @pytest.fixture
    def client(self) -> Client:
        return Client()

    class TestQuery:
        def test_http_error_is_raised_if_occurred(self, client):
            with requests_mock.Mocker() as m:
                m.post(BASE_URL, status_code=404)
                with pytest.raises(HTTPError):
                    client.query("")

        def test_exception_raised_for_none_200_response(self, client):
            with requests_mock.Mocker() as m:
                m.post(BASE_URL, status_code=301)
                with pytest.raises(
                    FlareExplorerNoneBadResponseCode,
                    match="Status code of 301 returned",
                ):
                    client.query("")

        def test_response_with_error_in_body_raises_exception(self, client):
            with requests_mock.Mocker() as m:
                m.post(
                    BASE_URL,
                    status_code=200,
                    json={
                        "data": {},
                        "errors": [
                            {
                                "locations": [{"column": 3, "line": 2}],
                                "message": "Address not found.",
                                "path": ["address"],
                            },
                            {
                                "locations": [{"column": 3, "line": 2}],
                                "message": "Second Error.",
                                "path": ["address"],
                            },
                        ],
                    },
                )
                with pytest.raises(
                    FlareExplorerQueryError,
                    match="[Address not found., Second Error.]",
                ):
                    client.query("")

        def test_response_with_empty_data_field_raises_exception(self, client):
            with requests_mock.Mocker() as m:
                m.post(
                    BASE_URL,
                    status_code=200,
                    json={
                        "data": {},
                        "errors": [],
                    },
                )
                with pytest.raises(
                    FlareExplorerQueryError,
                    match="Data field in response is empty",
                ):
                    client.query("")

        def test_json_is_returned_for_successful_request(self, client):
            with requests_mock.Mocker() as m:
                m.post(
                    BASE_URL,
                    status_code=200,
                    json={
                        "data": {"address": ["test"]},
                        "errors": [],
                    },
                )
                response = client.query("transaction(hash: asdf){}")

                assert m.last_request.json() == {"query": "transaction(hash: asdf){}"}
                assert response == {"address": ["test"]}
