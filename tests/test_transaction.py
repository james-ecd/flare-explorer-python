from decimal import Decimal

import requests_mock

from flare_explorer.gql_client import BASE_URL
from flare_explorer.transaction import (
    get_transaction_info,
    TransactionInfoResponse,
    InternalTransaction,
)


class TestInternalTransaction:
    class TestSerializeInternalTransactionsFromInfoResponse:
        def test_empty_transactions_given_returns_list(self):
            result = (
                InternalTransaction.serialize_internal_transactions_from_info_response(
                    {}
                )
            )
            assert result == []

        def test_internal_transactions_serialize_correctly(self):
            result = InternalTransaction.serialize_internal_transactions_from_info_response(
                {
                    "edges": [
                        {
                            "node": {
                                "fromAddressHash": "0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                                "input": "0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                                "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                "toAddressHash": "0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                            }
                        },
                        {
                            "node": {
                                "fromAddressHash": "0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                                "input": "0x92bfe6d80000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                                "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                "toAddressHash": "0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                            }
                        },
                        {
                            "node": {
                                "fromAddressHash": "0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                                "input": "0x4ee2cd7e0000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                                "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                "toAddressHash": "0x1d80c49bbbcd1c0911346656b529df9e5c2f783d",
                            }
                        },
                    ]
                }
            )
            assert result == [
                InternalTransaction(
                    input="0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                    output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                    toAddressHash="0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                    fromAddressHash="0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                ),
                InternalTransaction(
                    input="0x92bfe6d80000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                    output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                    toAddressHash="0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                    fromAddressHash="0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                ),
                InternalTransaction(
                    input="0x4ee2cd7e0000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                    output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                    toAddressHash="0x1d80c49bbbcd1c0911346656b529df9e5c2f783d",
                    fromAddressHash="0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                ),
            ]


class TestGetTransactionInfo:
    def test_query_is_built_correctly(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {"address": ["test"]},
                    "errors": [],
                },
            )
            try:
                get_transaction_info("test_hash_123", num_internal_transactions=100)
            except KeyError:
                # catch where get_transaction_info fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert 'transaction(hash: "test_hash_123")' in query
            assert "internalTransactions(first:100)" in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {
                        "transaction": {
                            "blockNumber": 4463469,
                            "createdContractAddressHash": None,
                            "cumulativeGasUsed": "85427",
                            "error": None,
                            "fromAddressHash": "0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                            "gas": "300000",
                            "gasPrice": "157368749629",
                            "gasUsed": "85427",
                            "hash": "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                            "id": "VHJhbnNhY3Rpb246MHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIy",
                            "index": 0,
                            "input": "0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                            "internalTransactions": {
                                "edges": [
                                    {
                                        "node": {
                                            "fromAddressHash": "0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                                            "input": "0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                                            "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                            "toAddressHash": "0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                                        }
                                    },
                                    {
                                        "node": {
                                            "fromAddressHash": "0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                                            "input": "0x92bfe6d80000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                                            "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                            "toAddressHash": "0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                                        }
                                    },
                                    {
                                        "node": {
                                            "fromAddressHash": "0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                                            "input": "0x4ee2cd7e0000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                                            "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                            "toAddressHash": "0x1d80c49bbbcd1c0911346656b529df9e5c2f783d",
                                        }
                                    },
                                ]
                            },
                            "nonce": "4",
                            "r": "16639664924577990513658501374748238325663514469127536284212373182223315423076",
                            "s": "8781023701017869979397360062628665986373158095147107542358445627839419564829",
                            "status": "OK",
                            "toAddressHash": "0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                            "v": "64",
                            "value": "0",
                        }
                    },
                    "errors": [],
                },
            )

            response = get_transaction_info(
                "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                num_internal_transactions=3,
            )

            assert response == TransactionInfoResponse(
                blockNumber=4463469,
                createdContractAddressHash=None,
                cumulativeGasUsed=Decimal("85427"),
                error=None,
                fromAddressHash="0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                gas=Decimal("300000"),
                gasPrice=Decimal("157368749629"),
                gasUsed=Decimal("85427"),
                hash="0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                id="VHJhbnNhY3Rpb246MHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIy",
                index=0,
                input="0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                nonce="4",
                r=Decimal(
                    "16639664924577990513658501374748238325663514469127536284212373182223315423076"
                ),
                s=Decimal(
                    "8781023701017869979397360062628665986373158095147107542358445627839419564829"
                ),
                status="OK",
                toAddressHash="0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                v=Decimal("64"),
                value=Decimal("0"),
                internalTransactions=[
                    InternalTransaction(
                        input="0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                        output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                        toAddressHash="0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                        fromAddressHash="0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                    ),
                    InternalTransaction(
                        input="0x92bfe6d80000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                        output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                        toAddressHash="0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                        fromAddressHash="0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                    ),
                    InternalTransaction(
                        input="0x4ee2cd7e0000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                        output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                        toAddressHash="0x1d80c49bbbcd1c0911346656b529df9e5c2f783d",
                        fromAddressHash="0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                    ),
                ],
            )
