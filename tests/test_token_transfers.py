from decimal import Decimal

import requests_mock

from flare_explorer import get_token_transfers
from flare_explorer.gql_client import BASE_URL, PageInfo
from flare_explorer.token_transfers import TokenTransfer


class TestGetTokenTransfers:
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
                get_token_transfers("hash", previous_cursor="prev")
            except KeyError:
                # catch where get_token_transfers fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert (
                'tokenTransfers(        first: 10       after: "prev"       tokenContractAddressHash: "hash"'
                in query
            )

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {
                        "tokenTransfers": {
                            "edges": [
                                {
                                    "node": {
                                        "amount": "495000000000000000000000000",
                                        "blockNumber": 4645423,
                                        "fromAddressHash": "0x85bbbe7c96e1060965b139c335c685860619189e",
                                        "id": "VG9rZW5UcmFuc2Zlcjp7ImxvZ19pbmRleCI6MCwidHJhbnNhY3Rpb25faGFzaCI6IjB4NjY5N2MxOTc4MzU3YmE5MDIyNzdjN2U2NDNiNTY2OGNlOWMwZTExMzE5ZGE5MmY3ODg0MTM4Mjg4MWQ0NjJmYyJ9",
                                        "logIndex": 0,
                                        "toAddressHash": "0x79241595ea6d3ec3ba0603027b51f5230ce265d0",
                                        "tokenContractAddressHash": "0xc18f99ce6dd6278be2d3f1e738ed11623444ae33",
                                        "tokenId": None,
                                        "transactionHash": "0x6697c1978357ba902277c7e643b5668ce9c0e11319da92f78841382881d462fc",
                                    }
                                },
                                {
                                    "node": {
                                        "amount": "5000000000000000000000000",
                                        "blockNumber": 4645423,
                                        "fromAddressHash": "0x85bbbe7c96e1060965b139c335c685860619189e",
                                        "id": "VG9rZW5UcmFuc2Zlcjp7ImxvZ19pbmRleCI6MSwidHJhbnNhY3Rpb25faGFzaCI6IjB4NjY5N2MxOTc4MzU3YmE5MDIyNzdjN2U2NDNiNTY2OGNlOWMwZTExMzE5ZGE5MmY3ODg0MTM4Mjg4MWQ0NjJmYyJ9",
                                        "logIndex": 1,
                                        "toAddressHash": "0x0000000000000000000000000000000000000000",
                                        "tokenContractAddressHash": "0xc18f99ce6dd6278be2d3f1e738ed11623444ae33",
                                        "tokenId": None,
                                        "transactionHash": "0x6697c1978357ba902277c7e643b5668ce9c0e11319da92f78841382881d462fc",
                                    }
                                },
                            ],
                            "pageInfo": {
                                "endCursor": "YXJyYXljb25uZWN0aW9uOjk=",
                                "hasNextPage": True,
                                "hasPreviousPage": False,
                                "startCursor": "YXJyYXljb25uZWN0aW9uOjA=",
                            },
                        }
                    }
                },
            )

            token_transfers, page_info = get_token_transfers(
                "0xC18f99CE6DD6278BE2D3f1e738Ed11623444aE33"
            )

            assert token_transfers == [
                TokenTransfer(
                    amount=Decimal("495000000000000000000000000"),
                    blockNumber=4645423,
                    fromAddressHash="0x85bbbe7c96e1060965b139c335c685860619189e",
                    id="VG9rZW5UcmFuc2Zlcjp7ImxvZ19pbmRleCI6MCwidHJhbnNhY3Rpb25faGFzaCI6IjB4NjY5N2MxOTc4MzU3YmE5MDIyNzdjN2U2NDNiNTY2OGNlOWMwZTExMzE5ZGE5MmY3ODg0MTM4Mjg4MWQ0NjJmYyJ9",
                    logIndex=0,
                    toAddressHash="0x79241595ea6d3ec3ba0603027b51f5230ce265d0",
                    tokenContractAddressHash="0xc18f99ce6dd6278be2d3f1e738ed11623444ae33",
                    tokenId=None,
                    transactionHash="0x6697c1978357ba902277c7e643b5668ce9c0e11319da92f78841382881d462fc",
                ),
                TokenTransfer(
                    amount=Decimal("5000000000000000000000000"),
                    blockNumber=4645423,
                    fromAddressHash="0x85bbbe7c96e1060965b139c335c685860619189e",
                    id="VG9rZW5UcmFuc2Zlcjp7ImxvZ19pbmRleCI6MSwidHJhbnNhY3Rpb25faGFzaCI6IjB4NjY5N2MxOTc4MzU3YmE5MDIyNzdjN2U2NDNiNTY2OGNlOWMwZTExMzE5ZGE5MmY3ODg0MTM4Mjg4MWQ0NjJmYyJ9",
                    logIndex=1,
                    toAddressHash="0x0000000000000000000000000000000000000000",
                    tokenContractAddressHash="0xc18f99ce6dd6278be2d3f1e738ed11623444ae33",
                    tokenId=None,
                    transactionHash="0x6697c1978357ba902277c7e643b5668ce9c0e11319da92f78841382881d462fc",
                ),
            ]

            assert page_info == PageInfo(
                endCursor="YXJyYXljb25uZWN0aW9uOjk=",
                hasNextPage=True,
                hasPreviousPage=False,
                startCursor="YXJyYXljb25uZWN0aW9uOjA=",
            )
