import pytest
import requests_mock
from requests import HTTPError

from flare_explorer.api import BASE_URL, Api
from flare_explorer.exceptions import (
    FlareExplorerNoneBadResponseCode,
    FlareExplorerQueryError,
)


class TestApi:
    @pytest.fixture
    def api(self) -> Api:
        return Api()

    class TestMakeRequest:
        def test_http_error_is_raised_if_occurred(self, api):
            with requests_mock.Mocker() as m:
                m.post(BASE_URL, status_code=404)
                with pytest.raises(HTTPError):
                    api.make_request("")

        def test_exception_raised_for_none_200_response(self, api):
            with requests_mock.Mocker() as m:
                m.post(BASE_URL, status_code=301)
                with pytest.raises(
                    FlareExplorerNoneBadResponseCode,
                    match="Status code of 301 returned",
                ):
                    api.make_request("")

        def test_response_with_error_in_body_raises_exception(self, api):
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
                    api.make_request("")

        def test_json_is_returned_for_successful_request(self, api):
            with requests_mock.Mocker() as m:
                m.post(
                    BASE_URL,
                    status_code=200,
                    json={
                        "data": {"address": ["test"]},
                        "errors": [],
                    },
                )
                response = api.make_request("transaction(hash: asdf){}")

                assert m.last_request.json() == {"query": "transaction(hash: asdf){}"}
                assert response == {
                    "data": {"address": ["test"]},
                    "errors": [],
                }
