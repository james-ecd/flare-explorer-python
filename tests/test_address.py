from decimal import Decimal

import requests_mock

from flare_explorer.address import AddressInfo, get_address_info
from flare_explorer.gql_client import BASE_URL


class TestGetAddressInfo:
    def test_query_is_built_correctly(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {"transaction": ["test"]},
                    "errors": [],
                },
            )
            try:
                get_address_info("test_hash_123")
            except KeyError:
                # catch where get_address_info fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert 'address(hash: "test_hash_123")' in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {
                        "address": {
                            "contractCode": None,
                            "fetchedCoinBalance": "1457768374895067448",
                            "fetchedCoinBalanceBlockNumber": 4497096,
                            "smartContract": {
                                "abi": "abi",
                                "addressHash": "hash",
                                "compilerVersion": "version1",
                                "contractSourceCode": "sourcecode",
                                "name": "name",
                                "optimization": True,
                            },
                        }
                    }
                },
            )

            response = get_address_info(
                "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
            )

            assert response == AddressInfo(
                contractCode=None,
                fetchedCoinBalance=Decimal("1457768374895067448"),
                fetchedCoinBalanceBlockNumber=4497096,
                smartContract={
                    "abi": "abi",
                    "addressHash": "hash",
                    "compilerVersion": "version1",
                    "contractSourceCode": "sourcecode",
                    "name": "name",
                    "optimization": True,
                },
            )
