from decimal import Decimal

import requests_mock

from flare_explorer.gql_client import BASE_URL, PageInfo
from flare_explorer.transaction import (
    InternalTransaction,
    TransactionInfo,
    get_internal_transactions,
    get_transaction_info,
)


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
                get_transaction_info("test_hash_123")
            except KeyError:
                # catch where get_transaction_info fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert 'transaction(hash: "test_hash_123")' in query

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
            )

            assert response == TransactionInfo(
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
            )


class TestGetInternalTransactions:
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
                get_internal_transactions("hash", previous_cursor="prev")
            except TypeError:
                # catch where get_internal_transactions fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert 'transaction(hash: "hash"){' in query
            assert 'internalTransactions(first: 5 after: "prev"' in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {
                        "transaction": {
                            "internalTransactions": {
                                "edges": [
                                    {
                                        "node": {
                                            "blockNumber": 4463469,
                                            "callType": "CALL",
                                            "createdContractAddressHash": None,
                                            "createdContractCode": None,
                                            "error": None,
                                            "fromAddressHash": "0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                                            "gas": "278284",
                                            "gasUsed": "63711",
                                            "id": "SW50ZXJuYWxUcmFuc2FjdGlvbjp7ImluZGV4IjowLCJ0cmFuc2FjdGlvbl9oYXNoIjoiMHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIyIn0=",
                                            "index": 0,
                                            "init": None,
                                            "input": "0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                                            "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                            "toAddressHash": "0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                                            "traceAddress": "[]",
                                            "transactionHash": "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                                            "transactionIndex": 0,
                                            "type": "CALL",
                                            "value": "0",
                                        }
                                    },
                                    {
                                        "node": {
                                            "blockNumber": 4463469,
                                            "callType": "STATICCALL",
                                            "createdContractAddressHash": None,
                                            "createdContractCode": None,
                                            "error": None,
                                            "fromAddressHash": "0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                                            "gas": "259698",
                                            "gasUsed": "15604",
                                            "id": "SW50ZXJuYWxUcmFuc2FjdGlvbjp7ImluZGV4IjoxLCJ0cmFuc2FjdGlvbl9oYXNoIjoiMHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIyIn0=",
                                            "index": 1,
                                            "init": None,
                                            "input": "0x92bfe6d80000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                                            "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                            "toAddressHash": "0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                                            "traceAddress": "[0]",
                                            "transactionHash": "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                                            "transactionIndex": 0,
                                            "type": "CALL",
                                            "value": "0",
                                        }
                                    },
                                    {
                                        "node": {
                                            "blockNumber": 4463469,
                                            "callType": "STATICCALL",
                                            "createdContractAddressHash": None,
                                            "createdContractCode": None,
                                            "error": None,
                                            "fromAddressHash": "0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                                            "gas": "247725",
                                            "gasUsed": "7410",
                                            "id": "SW50ZXJuYWxUcmFuc2FjdGlvbjp7ImluZGV4IjoyLCJ0cmFuc2FjdGlvbl9oYXNoIjoiMHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIyIn0=",
                                            "index": 2,
                                            "init": None,
                                            "input": "0x4ee2cd7e0000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                                            "output": "0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                                            "toAddressHash": "0x1d80c49bbbcd1c0911346656b529df9e5c2f783d",
                                            "traceAddress": "[0,0]",
                                            "transactionHash": "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                                            "transactionIndex": 0,
                                            "type": "CALL",
                                            "value": "0",
                                        }
                                    },
                                ],
                                "pageInfo": {
                                    "endCursor": "YXJyYXljb25uZWN0aW9uOjI=",
                                    "hasNextPage": False,
                                    "hasPreviousPage": True,
                                    "startCursor": "YXJyYXljb25uZWN0aW9uOjE=",
                                },
                            }
                        }
                    }
                },
            )

            internal_transactions, page_info = get_internal_transactions(
                "0xC18f99CE6DD6278BE2D3f1e738Ed11623444aE33"
            )

            assert internal_transactions == [
                InternalTransaction(
                    blockNumber=4463469,
                    callType="CALL",
                    createdContractAddressHash=None,
                    createdContractCode=None,
                    error=None,
                    fromAddressHash="0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                    gas=Decimal("278284"),
                    gasUsed=Decimal("63711"),
                    id="SW50ZXJuYWxUcmFuc2FjdGlvbjp7ImluZGV4IjowLCJ0cmFuc2FjdGlvbl9oYXNoIjoiMHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIyIn0=",
                    index=0,
                    init=None,
                    input="0x56781388453aa8084d7436d8f245536c1c81f77ca93f8d97e67cd8ffc23890a5bc8c53850000000000000000000000000000000000000000000000000000000000000001",
                    output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                    toAddressHash="0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                    traceAddress="[]",
                    transactionHash="0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                    transactionIndex=0,
                    type="CALL",
                    value=Decimal("0"),
                ),
                InternalTransaction(
                    blockNumber=4463469,
                    callType="STATICCALL",
                    createdContractAddressHash=None,
                    createdContractCode=None,
                    error=None,
                    fromAddressHash="0x258e20bdbb2d891521308d2af381b1bd962b67b5",
                    gas=Decimal("259698"),
                    gasUsed=Decimal("15604"),
                    id="SW50ZXJuYWxUcmFuc2FjdGlvbjp7ImluZGV4IjoxLCJ0cmFuc2FjdGlvbl9oYXNoIjoiMHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIyIn0=",
                    index=1,
                    init=None,
                    input="0x92bfe6d80000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                    output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                    toAddressHash="0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                    traceAddress="[0]",
                    transactionHash="0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                    transactionIndex=0,
                    type="CALL",
                    value=Decimal("0"),
                ),
                InternalTransaction(
                    blockNumber=4463469,
                    callType="STATICCALL",
                    createdContractAddressHash=None,
                    createdContractCode=None,
                    error=None,
                    fromAddressHash="0x47dd40dedcda8b4efdef5101999af33b7cf787d7",
                    gas=Decimal("247725"),
                    gasUsed=Decimal("7410"),
                    id="SW50ZXJuYWxUcmFuc2FjdGlvbjp7ImluZGV4IjoyLCJ0cmFuc2FjdGlvbl9oYXNoIjoiMHgwM2MxOWMxMzE5NWM3YTg1YWZmYmVjZWExODZiMjUzZTU4MDExZjc2YTE2MDQ4OWJiZmJhZDI0NGY5NjllZWIyIn0=",
                    index=2,
                    init=None,
                    input="0x4ee2cd7e0000000000000000000000004668b6ec17d7e6a0cbf600b68ec4f04ae45d225e000000000000000000000000000000000000000000000000000000000042a029",
                    output="0x0000000000000000000000000000000000000000000000e6047124000d1f6775",
                    toAddressHash="0x1d80c49bbbcd1c0911346656b529df9e5c2f783d",
                    traceAddress="[0,0]",
                    transactionHash="0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
                    transactionIndex=0,
                    type="CALL",
                    value=Decimal("0"),
                ),
            ]

            assert page_info == PageInfo(
                endCursor="YXJyYXljb25uZWN0aW9uOjI=",
                hasNextPage=False,
                hasPreviousPage=True,
                startCursor="YXJyYXljb25uZWN0aW9uOjE=",
            )
