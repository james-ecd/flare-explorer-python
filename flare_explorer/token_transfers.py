from decimal import Decimal

from pydantic import BaseModel

from flare_explorer.gql_client import (
    Client,
    PageInfo,
    generate_after_pagination_query_line,
)


class TokenTransfer(BaseModel):
    amount: Decimal
    blockNumber: int
    fromAddressHash: str
    id: str
    logIndex: int
    toAddressHash: str
    tokenContractAddressHash: str
    tokenId: Decimal | None
    transactionHash: str


def get_token_transfers(
    token_contract_address_hash: str, previous_cursor: str | None = None
) -> ([TokenTransfer], PageInfo):
    """
    Get token transfers for a given contract address hash.
    Returns in pages of size 10
    Args:
        token_contract_address_hash: contract address hash
        previous_cursor: final cursor of the previous page

    Returns:
        Tuple[
            list of token transfers,
            pagination page info
        ]
    """
    query = (
        "{"
        "    tokenTransfers("
        "        first: 10"
        f"       {generate_after_pagination_query_line(previous_cursor)}"
        f'       tokenContractAddressHash: "{token_contract_address_hash}"'
        "    ){"
        "        edges {"
        "            node {"
        "                amount"
        "                blockNumber"
        "                fromAddressHash"
        "                id"
        "                logIndex"
        "                toAddressHash"
        "                tokenContractAddressHash"
        "                tokenId"
        "                transactionHash"
        "            }"
        "        }"
        "        pageInfo {"
        "            endCursor"
        "            hasNextPage"
        "            hasPreviousPage"
        "            startCursor"
        "        }"
        "    }"
        "}"
    )
    response = Client().query(query)["tokenTransfers"]
    return [TokenTransfer(**i["node"]) for i in response["edges"]], PageInfo(
        **response["pageInfo"]
    )
