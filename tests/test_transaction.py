import contextlib
from decimal import Decimal

import requests_mock

from flare_explorer.gql_client import API_URL, PageInfo
from flare_explorer.transaction import (
    InternalTransaction,
    Transaction,
    get_internal_transactions,
    get_transaction,
    get_transactions_from_address,
)


class TestGetTransaction:
    def test_query_is_built_correctly(self):
        with requests_mock.Mocker() as m:
            m.post(
                API_URL,
                status_code=200,
                json={
                    "data": {"address": ["test"]},
                    "errors": [],
                },
            )
            with contextlib.suppress(KeyError):
                get_transaction("test_hash_123")

            query = m.last_request.json()["query"]
            assert 'transaction(hash: "test_hash_123")' in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                API_URL,
                status_code=200,
                json={
                    "data": {
                        "transaction": {
                            "blockNumber": 4463469,
                            "createdContractAddressHash": None,
                            "cumulativeGasUsed": "85427",
                            "error": None,
                            "fromAddressHash": (
                                "0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e"
                            ),
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
                            "toAddressHash": (
                                "0x258e20bdbb2d891521308d2af381b1bd962b67b5"
                            ),
                            "v": "64",
                            "value": "0",
                        }
                    },
                    "errors": [],
                },
            )

            response = get_transaction(
                "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2",
            )

            assert response == Transaction(
                blockNumber=4463469,
                createdContractAddressHash=None,
                cumulativeGasUsed=Decimal("85427"),
                error=None,
                fromAddressHash="0x4668b6ec17d7e6a0cbf600b68ec4f04ae45d225e",
                gas=Decimal("300000"),
                gasPrice=Decimal("157368749629"),
                gasUsed=Decimal("85427"),
                hash=(
                    "0x03c19c13195c7a85affbecea186b253e58011f76a160489bbfbad244f969eeb2"
                ),
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
                API_URL,
                status_code=200,
                json={
                    "data": {"transaction": ["test"]},
                    "errors": [],
                },
            )
            with contextlib.suppress(TypeError):
                get_internal_transactions("hash", previous_cursor="prev")

            query = m.last_request.json()["query"]
            assert 'transaction(hash: "hash") {' in query
            assert 'internalTransactions(first: 5, after: "prev") {' in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                API_URL,
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


class TestGetTransactionsFromAddress:
    def test_query_is_built_correctly(self):
        with requests_mock.Mocker() as m:
            m.post(
                API_URL,
                status_code=200,
                json={
                    "data": {"transaction": ["test"]},
                    "errors": [],
                },
            )
            with contextlib.suppress(KeyError):
                get_transactions_from_address("hash", previous_cursor="prev")

            query = m.last_request.json()["query"]
            assert 'address(hash: "hash") {' in query
            assert 'transactions(first: 5, after: "prev") {' in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                API_URL,
                status_code=200,
                json={
                    "data": {
                        "address": {
                            "transactions": {
                                "edges": [
                                    {
                                        "node": {
                                            "blockNumber": 4683168,
                                            "createdContractAddressHash": None,
                                            "cumulativeGasUsed": "110685",
                                            "error": None,
                                            "fromAddressHash": "0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                                            "gas": "121753",
                                            "gasPrice": "156276191310",
                                            "gasUsed": "110685",
                                            "hash": "0x0673caa4ae1a3d4398409ec3a237fac9602b1793053735e830ce33a245fa9724",
                                            "id": "VHJhbnNhY3Rpb246MHgwNjczY2FhNGFlMWEzZDQzOTg0MDllYzNhMjM3ZmFjOTYwMmIxNzkzMDUzNzM1ZTgzMGNlMzNhMjQ1ZmE5NzI0",
                                            "index": 0,
                                            "input": "0x7b0472f000000000000000000000000000000000000000000000000000000000000000b80000000000000000000000000000000000000000000000de541f2c1f7fd14c8b",
                                            "nonce": "116",
                                            "r": "69110172682335806364040708819255236652964624184738950468338136220819860526097",
                                            "s": "24438838221371425490022239267178137476597952062998375067614947913018301517845",
                                            "status": "OK",
                                            "toAddressHash": "0x12245b3fe351ec3be15ef971f31927af1292ff40",
                                            "v": "64",
                                            "value": "0",
                                        }
                                    },
                                    {
                                        "node": {
                                            "blockNumber": 4683146,
                                            "createdContractAddressHash": None,
                                            "cumulativeGasUsed": "999487",
                                            "error": None,
                                            "fromAddressHash": "0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                                            "gas": "377732",
                                            "gasPrice": "161831433505",
                                            "gasUsed": "340502",
                                            "hash": "0xe6a938216dda32db681ab0ef8a14686b49548f1227f959bedd4329b616c05d17",
                                            "id": "VHJhbnNhY3Rpb246MHhlNmE5MzgyMTZkZGEzMmRiNjgxYWIwZWY4YTE0Njg2YjQ5NTQ4ZjEyMjdmOTU5YmVkZDQzMjliNjE2YzA1ZDE3",
                                            "index": 1,
                                            "input": "0x38ed17390000000000000000000000000000000000000000000001830f67aaa8a11000000000000000000000000000000000000000000000000000dd38f4fcc77644288000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000ca4599ae99cc0e11ecb2085a9b9458e56a5558660000000000000000000000000000000000000000000000000000000063d4edce00000000000000000000000000000000000000000000000000000000000000020000000000000000000000001d80c49bbbcd1c0911346656b529df9e5c2f783d000000000000000000000000b5010d5eb31aa8776b52c7394b76d6d627501c73",
                                            "nonce": "115",
                                            "r": "68263596489818068273490042162762780137126232110296704047257006488064843753916",
                                            "s": "44456617425739706583626663352120306925984958454311645537448164230033079209049",
                                            "status": "OK",
                                            "toAddressHash": "0xa981cb468c87ed32f37de546e25a7c5ff17e2308",
                                            "v": "63",
                                            "value": "0",
                                        }
                                    },
                                    {
                                        "node": {
                                            "blockNumber": 4667097,
                                            "createdContractAddressHash": None,
                                            "cumulativeGasUsed": "318905",
                                            "error": None,
                                            "fromAddressHash": "0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                                            "gas": "357262",
                                            "gasPrice": "161905172630",
                                            "gasUsed": "318905",
                                            "hash": "0x025955739824d3aab8c64d5dc45dd4e61378236ef0d45b90eb4e028e1d9dc7b6",
                                            "id": "VHJhbnNhY3Rpb246MHgwMjU5NTU3Mzk4MjRkM2FhYjhjNjRkNWRjNDVkZDRlNjEzNzgyMzZlZjBkNDViOTBlYjRlMDI4ZTFkOWRjN2I2",
                                            "index": 0,
                                            "input": "0x38ed1739000000000000000000000000000000000000000000000593370b94e43876f7b10000000000000000000000000000000000000000000008bae44b5278e6e9bef700000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000ca4599ae99cc0e11ecb2085a9b9458e56a5558660000000000000000000000000000000000000000000000000000000063d45af10000000000000000000000000000000000000000000000000000000000000002000000000000000000000000b5010d5eb31aa8776b52c7394b76d6d627501c730000000000000000000000001d80c49bbbcd1c0911346656b529df9e5c2f783d",
                                            "nonce": "114",
                                            "r": "74484998305257084337759328853945129582419663529275305463115324862399392793074",
                                            "s": "1411060812467440587137039572906739078207298153190888655500475205913938557276",
                                            "status": "OK",
                                            "toAddressHash": "0xa981cb468c87ed32f37de546e25a7c5ff17e2308",
                                            "v": "64",
                                            "value": "0",
                                        }
                                    },
                                    {
                                        "node": {
                                            "blockNumber": 4667074,
                                            "createdContractAddressHash": None,
                                            "cumulativeGasUsed": "107905",
                                            "error": None,
                                            "fromAddressHash": "0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                                            "gas": "118695",
                                            "gasPrice": "156221400610",
                                            "gasUsed": "107905",
                                            "hash": "0x98c107acf618b865d3bfc1b251e02d817b91d60ec390ac72e77d0f8a5eaabd5c",
                                            "id": "VHJhbnNhY3Rpb246MHg5OGMxMDdhY2Y2MThiODY1ZDNiZmMxYjI1MWUwMmQ4MTdiOTFkNjBlYzM5MGFjNzJlNzdkMGY4YTVlYWFiZDVj",
                                            "index": 0,
                                            "input": "0x441a3e7000000000000000000000000000000000000000000000000000000000000000b800000000000000000000000000000000000000000000059309a9cadfb6bc0b7b",
                                            "nonce": "113",
                                            "r": "55248785083710694235808323489612913142618133995267024812984365158299293090761",
                                            "s": "2048702665417996508651634995795299213095176961067465521096902431328902020172",
                                            "status": "OK",
                                            "toAddressHash": "0x12245b3fe351ec3be15ef971f31927af1292ff40",
                                            "v": "64",
                                            "value": "0",
                                        }
                                    },
                                    {
                                        "node": {
                                            "blockNumber": 4666468,
                                            "createdContractAddressHash": None,
                                            "cumulativeGasUsed": "70492",
                                            "error": None,
                                            "fromAddressHash": "0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                                            "gas": "77541",
                                            "gasPrice": "185885784109",
                                            "gasUsed": "70492",
                                            "hash": "0xf472bd6851b72bca48f4b00de3b9a61b430f931ce5cef694b19f3cf1ea27ca66",
                                            "id": "VHJhbnNhY3Rpb246MHhmNDcyYmQ2ODUxYjcyYmNhNDhmNGIwMGRlM2I5YTYxYjQzMGY5MzFjZTVjZWY2OTRiMTlmM2NmMWVhMjdjYTY2",
                                            "index": 0,
                                            "input": "0xaa5f7e2600000000000000000000000000000000000000000000000000000000000000b8",
                                            "nonce": "112",
                                            "r": "88984618453470261412210791100386178155102370485203816039147431088908816075419",
                                            "s": "57024215636583135282092645337517604904032658973181163770974371052340296504527",
                                            "status": "OK",
                                            "toAddressHash": "0x12245b3fe351ec3be15ef971f31927af1292ff40",
                                            "v": "63",
                                            "value": "0",
                                        }
                                    },
                                ],
                                "pageInfo": {
                                    "endCursor": "YXJyYXljb25uZWN0aW9uOjQ=",
                                    "hasNextPage": True,
                                    "hasPreviousPage": False,
                                    "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
                                },
                            }
                        }
                    }
                },
            )

            transactions, page_info = get_transactions_from_address(
                "0xC18f99CE6DD6278BE2D3f1e738Ed11623444aE33"
            )

            assert transactions == [
                Transaction(
                    blockNumber=4683168,
                    createdContractAddressHash=None,
                    cumulativeGasUsed=Decimal("110685"),
                    error=None,
                    fromAddressHash="0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                    gas=Decimal("121753"),
                    gasPrice=Decimal("156276191310"),
                    gasUsed=Decimal("110685"),
                    hash="0x0673caa4ae1a3d4398409ec3a237fac9602b1793053735e830ce33a245fa9724",
                    id="VHJhbnNhY3Rpb246MHgwNjczY2FhNGFlMWEzZDQzOTg0MDllYzNhMjM3ZmFjOTYwMmIxNzkzMDUzNzM1ZTgzMGNlMzNhMjQ1ZmE5NzI0",
                    index=0,
                    input="0x7b0472f000000000000000000000000000000000000000000000000000000000000000b80000000000000000000000000000000000000000000000de541f2c1f7fd14c8b",
                    nonce="116",
                    r=Decimal(
                        "69110172682335806364040708819255236652964624184738950468338136220819860526097"
                    ),
                    s=Decimal(
                        "24438838221371425490022239267178137476597952062998375067614947913018301517845"
                    ),
                    status="OK",
                    toAddressHash="0x12245b3fe351ec3be15ef971f31927af1292ff40",
                    v=Decimal("64"),
                    value=Decimal("0"),
                ),
                Transaction(
                    blockNumber=4683146,
                    createdContractAddressHash=None,
                    cumulativeGasUsed=Decimal("999487"),
                    error=None,
                    fromAddressHash="0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                    gas=Decimal("377732"),
                    gasPrice=Decimal("161831433505"),
                    gasUsed=Decimal("340502"),
                    hash="0xe6a938216dda32db681ab0ef8a14686b49548f1227f959bedd4329b616c05d17",
                    id="VHJhbnNhY3Rpb246MHhlNmE5MzgyMTZkZGEzMmRiNjgxYWIwZWY4YTE0Njg2YjQ5NTQ4ZjEyMjdmOTU5YmVkZDQzMjliNjE2YzA1ZDE3",
                    index=1,
                    input="0x38ed17390000000000000000000000000000000000000000000001830f67aaa8a11000000000000000000000000000000000000000000000000000dd38f4fcc77644288000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000ca4599ae99cc0e11ecb2085a9b9458e56a5558660000000000000000000000000000000000000000000000000000000063d4edce00000000000000000000000000000000000000000000000000000000000000020000000000000000000000001d80c49bbbcd1c0911346656b529df9e5c2f783d000000000000000000000000b5010d5eb31aa8776b52c7394b76d6d627501c73",
                    nonce="115",
                    r=Decimal(
                        "68263596489818068273490042162762780137126232110296704047257006488064843753916"
                    ),
                    s=Decimal(
                        "44456617425739706583626663352120306925984958454311645537448164230033079209049"
                    ),
                    status="OK",
                    toAddressHash="0xa981cb468c87ed32f37de546e25a7c5ff17e2308",
                    v=Decimal("63"),
                    value=Decimal("0"),
                ),
                Transaction(
                    blockNumber=4667097,
                    createdContractAddressHash=None,
                    cumulativeGasUsed=Decimal("318905"),
                    error=None,
                    fromAddressHash="0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                    gas=Decimal("357262"),
                    gasPrice=Decimal("161905172630"),
                    gasUsed=Decimal("318905"),
                    hash="0x025955739824d3aab8c64d5dc45dd4e61378236ef0d45b90eb4e028e1d9dc7b6",
                    id="VHJhbnNhY3Rpb246MHgwMjU5NTU3Mzk4MjRkM2FhYjhjNjRkNWRjNDVkZDRlNjEzNzgyMzZlZjBkNDViOTBlYjRlMDI4ZTFkOWRjN2I2",
                    index=0,
                    input="0x38ed1739000000000000000000000000000000000000000000000593370b94e43876f7b10000000000000000000000000000000000000000000008bae44b5278e6e9bef700000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000ca4599ae99cc0e11ecb2085a9b9458e56a5558660000000000000000000000000000000000000000000000000000000063d45af10000000000000000000000000000000000000000000000000000000000000002000000000000000000000000b5010d5eb31aa8776b52c7394b76d6d627501c730000000000000000000000001d80c49bbbcd1c0911346656b529df9e5c2f783d",
                    nonce="114",
                    r=Decimal(
                        "74484998305257084337759328853945129582419663529275305463115324862399392793074"
                    ),
                    s=Decimal(
                        "1411060812467440587137039572906739078207298153190888655500475205913938557276"
                    ),
                    status="OK",
                    toAddressHash="0xa981cb468c87ed32f37de546e25a7c5ff17e2308",
                    v=Decimal("64"),
                    value=Decimal("0"),
                ),
                Transaction(
                    blockNumber=4667074,
                    createdContractAddressHash=None,
                    cumulativeGasUsed=Decimal("107905"),
                    error=None,
                    fromAddressHash="0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                    gas=Decimal("118695"),
                    gasPrice=Decimal("156221400610"),
                    gasUsed=Decimal("107905"),
                    hash="0x98c107acf618b865d3bfc1b251e02d817b91d60ec390ac72e77d0f8a5eaabd5c",
                    id="VHJhbnNhY3Rpb246MHg5OGMxMDdhY2Y2MThiODY1ZDNiZmMxYjI1MWUwMmQ4MTdiOTFkNjBlYzM5MGFjNzJlNzdkMGY4YTVlYWFiZDVj",
                    index=0,
                    input="0x441a3e7000000000000000000000000000000000000000000000000000000000000000b800000000000000000000000000000000000000000000059309a9cadfb6bc0b7b",
                    nonce="113",
                    r=Decimal(
                        "55248785083710694235808323489612913142618133995267024812984365158299293090761"
                    ),
                    s=Decimal(
                        "2048702665417996508651634995795299213095176961067465521096902431328902020172"
                    ),
                    status="OK",
                    toAddressHash="0x12245b3fe351ec3be15ef971f31927af1292ff40",
                    v=Decimal("64"),
                    value=Decimal("0"),
                ),
                Transaction(
                    blockNumber=4666468,
                    createdContractAddressHash=None,
                    cumulativeGasUsed=Decimal("70492"),
                    error=None,
                    fromAddressHash="0xca4599ae99cc0e11ecb2085a9b9458e56a555866",
                    gas=Decimal("77541"),
                    gasPrice=Decimal("185885784109"),
                    gasUsed=Decimal("70492"),
                    hash="0xf472bd6851b72bca48f4b00de3b9a61b430f931ce5cef694b19f3cf1ea27ca66",
                    id="VHJhbnNhY3Rpb246MHhmNDcyYmQ2ODUxYjcyYmNhNDhmNGIwMGRlM2I5YTYxYjQzMGY5MzFjZTVjZWY2OTRiMTlmM2NmMWVhMjdjYTY2",
                    index=0,
                    input="0xaa5f7e2600000000000000000000000000000000000000000000000000000000000000b8",
                    nonce="112",
                    r=Decimal(
                        "88984618453470261412210791100386178155102370485203816039147431088908816075419"
                    ),
                    s=Decimal(
                        "57024215636583135282092645337517604904032658973181163770974371052340296504527"
                    ),
                    status="OK",
                    toAddressHash="0x12245b3fe351ec3be15ef971f31927af1292ff40",
                    v=Decimal("63"),
                    value=Decimal("0"),
                ),
            ]

            assert page_info == PageInfo(
                endCursor="YXJyYXljb25uZWN0aW9uOjQ=",
                hasNextPage=True,
                hasPreviousPage=False,
                startCursor="YXJyYXljb25uZWN0aW9uOjA=",
            )
