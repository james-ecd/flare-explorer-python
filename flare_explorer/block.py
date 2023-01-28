from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from flare_explorer.gql_client import Client


class Block(BaseModel):
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


def get_block(block_number: int) -> Block:
    """
    Get information about a given block
    Args:
        block_number: number of the block

    Returns:
        Information about the block
    """
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
    return Block(**response["block"])
