from decimal import Decimal

import pytest
import requests_mock

from flare_explorer.address import Address, SmartContract, get_address, get_addresses
from flare_explorer.exceptions import QueryComplexityLimit
from flare_explorer.gql_client import BASE_URL


class TestGetAddress:
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
                get_address("test_hash_123")
            except KeyError:
                # catch where get_address_info fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert 'address(hash: "test_hash_123") {' in query

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

            response = get_address(
                "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
            )

            assert response == Address(
                contractCode=None,
                fetchedCoinBalance=Decimal("1457768374895067448"),
                fetchedCoinBalanceBlockNumber=4497096,
                smartContract=SmartContract(
                    abi="abi",
                    addressHash="hash",
                    compilerVersion="version1",
                    contractSourceCode="sourcecode",
                    name="name",
                    optimization=True,
                ),
            )


class TestGetAddresses:
    def test_more_than_15_addresses_given_raises_exception(self):
        with pytest.raises(
            QueryComplexityLimit, match="Limit of 15 addresses breached"
        ):
            get_addresses([f"{i}" for i in range(16)])

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
                get_addresses(
                    [
                        "hash_1",
                        "hash_2",
                        "hash_3",
                    ]
                )
            except KeyError:
                # catch where get_address_info fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert 'addresses(hashes: ["hash_1","hash_2","hash_3"]) {' in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {
                        "addresses": [
                            {
                                "contractCode": None,
                                "fetchedCoinBalance": "296941861326935666031",
                                "fetchedCoinBalanceBlockNumber": 4686942,
                                "hash": "0x7736748e4b61b574d452100efbc69c140ff430cf",
                                "smartContract": None,
                            },
                            {
                                "contractCode": "contract_code",
                                "fetchedCoinBalance": "0",
                                "fetchedCoinBalanceBlockNumber": 4685648,
                                "hash": "0xc18f99ce6dd6278be2d3f1e738ed11623444ae33",
                                "smartContract": {
                                    "abi": "abi",
                                    "addressHash": (
                                        "0xc18f99ce6dd6278be2d3f1e738ed11623444ae33"
                                    ),
                                    "compilerVersion": "v0.5.17+commit.d19bba13",
                                    "contractSourceCode": "source_code",
                                    "name": "PoodleCoin",
                                    "optimization": False,
                                },
                            },
                        ]
                    }
                },
            )

            response = get_addresses(
                [
                    "0x7736748e4b61b574d452100efbc69c140ff430cf",
                    "0xc18f99ce6dd6278be2d3f1e738ed11623444ae33",
                ]
            )

            assert response == [
                Address(
                    contractCode=None,
                    fetchedCoinBalance=Decimal("296941861326935666031"),
                    fetchedCoinBalanceBlockNumber=4686942,
                    smartContract=None,
                ),
                Address(
                    contractCode="contract_code",
                    fetchedCoinBalance=Decimal("0"),
                    fetchedCoinBalanceBlockNumber=4685648,
                    smartContract=SmartContract(
                        abi="abi",
                        addressHash="0xc18f99ce6dd6278be2d3f1e738ed11623444ae33",
                        compilerVersion="v0.5.17+commit.d19bba13",
                        contractSourceCode="source_code",
                        name="PoodleCoin",
                        optimization=False,
                    ),
                ),
            ]
