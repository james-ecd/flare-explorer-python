from decimal import Decimal

from pydantic import BaseModel

from flare_explorer.gql_client import Client, PageInfo


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
    after_query = f'after: "{previous_cursor}"' if previous_cursor else ""
    query = (
        "{"
        "    tokenTransfers("
        "        first: 10"
        f"       {after_query}"
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
