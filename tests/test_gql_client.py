import pytest
import requests_mock
from gql.transport.exceptions import TransportQueryError

from flare_explorer.exceptions import FlareExplorerQueryError
from flare_explorer.gql_client import (
    API_URL,
    Client,
    generate_after_pagination_query_line,
)


@pytest.mark.parametrize(
    "previous_cursor,expected_query_line",
    [
        ("", ""),
        (None, ""),
        ("prev_cursor", 'after: "prev_cursor"'),
    ],
)
def test_generate_after_pagination_query_line(previous_cursor, expected_query_line):
    result = generate_after_pagination_query_line(previous_cursor)
    assert result == expected_query_line


class TestClient:
    @pytest.fixture
    def client(self) -> Client:
        return Client()

    class TestQuery:
        def test_response_with_error_in_body_raises_exception(self, client):
            with requests_mock.Mocker() as m:
                m.post(
                    API_URL,
                    status_code=200,
                    json={
                        "data": {},
                        "errors": [
                            {
                                "locations": [{"column": 3, "line": 2}],
                                "message": "Address not found.",
                                "path": ["address"],
                            },
                        ],
                    },
                )
                with pytest.raises(
                    TransportQueryError,
                ):
                    client.query("{address {contractCode}}")

        def test_empty_response_raises_exception(self, client):
            with requests_mock.Mocker() as m:
                m.post(
                    API_URL,
                    status_code=200,
                    json={
                        "data": {},
                        "errors": [],
                    },
                )
                with pytest.raises(
                    FlareExplorerQueryError, match="Data field in response is empty"
                ):
                    client.query("{address {contractCode}}")

        def test_json_is_returned_for_successful_request(self, client):
            with requests_mock.Mocker() as m:
                m.post(
                    API_URL,
                    status_code=200,
                    json={
                        "data": {"address": ["test"]},
                        "errors": [],
                    },
                )
                response = client.query("{transaction(hash: asdf){id}}")

                assert response == {"address": ["test"]}
