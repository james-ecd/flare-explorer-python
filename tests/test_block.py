from datetime import datetime, timezone
from decimal import Decimal

import requests_mock

from flare_explorer.block import get_block_info, BlockInfo
from flare_explorer.gql_client import BASE_URL


class TestGetBlockInfo:
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
                get_block_info(123)
            except KeyError:
                # catch where get_block_info fails to serialize mis-built response
                pass

            query = m.last_request.json()["query"]
            assert "block(number: 123)" in query

    def test_response_is_serialized_correctly_for_correct_response(self):
        with requests_mock.Mocker() as m:
            m.post(
                BASE_URL,
                status_code=200,
                json={
                    "data": {
                        "block": {
                            "consensus": True,
                            "difficulty": "1",
                            "gasLimit": "8000000",
                            "gasUsed": "85427",
                            "hash": "0x39935d7674e2f031fb69e617fc4a409960378a8953f346517a6124c26be86fee",
                            "minerHash": "0x0100000000000000000000000000000000000000",
                            "nonce": "0x0000000000000000",
                            "number": 4463469,
                            "parentHash": "0xaf474d4cf6ceaf5d1aa69b4789c3bfca337395968ccd1f9a85ca6927479cd467",
                            "size": 814,
                            "timestamp": "2023-01-22T15:54:20.000000Z",
                            "totalDifficulty": "4463469",
                        }
                    }
                },
            )

            response = get_block_info(4463469)

            assert response == BlockInfo(
                consensus=True,
                difficulty=Decimal("1"),
                gasLimit=Decimal("8000000"),
                gasUsed=Decimal("85427"),
                hash="0x39935d7674e2f031fb69e617fc4a409960378a8953f346517a6124c26be86fee",
                minerHash="0x0100000000000000000000000000000000000000",
                nonce="0x0000000000000000",
                number=4463469,
                parentHash="0xaf474d4cf6ceaf5d1aa69b4789c3bfca337395968ccd1f9a85ca6927479cd467",
                size=814,
                timestamp=datetime(2023, 1, 22, 15, 54, 20, tzinfo=timezone.utc),
                totalDifficulty=Decimal("4463469"),
            )
