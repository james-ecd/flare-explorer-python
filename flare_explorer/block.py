from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from flare_explorer.gql_client import Client


class BlockInfo(BaseModel):
    consensus: bool
    difficulty: Decimal
    gasLimit: Decimal
    gasUsed: Decimal
    hash: str
    minerHash: str
    nonce: str
    number: int
    parentHash: str
    size: int
    timestamp: datetime
    totalDifficulty: Decimal


def get_block_info(block_number: int) -> BlockInfo:
    query = (
        "{"
        f"    block(number: {block_number}) {{"
        "        consensus"
        "        difficulty"
        "        gasLimit"
        "        gasUsed"
        "        hash"
        "        minerHash"
        "        nonce"
        "        number"
        "        parentHash"
        "        size"
        "        timestamp"
        "        totalDifficulty"
        "    }"
        "}"
    )
    response = Client().query(query)
    return BlockInfo(**response["block"])
