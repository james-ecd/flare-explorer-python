from decimal import Decimal

from pydantic import BaseModel

from flare_explorer.gql_client import (
    Client,
    PageInfo,
    generate_after_pagination_query_line,
)


class InternalTransaction(BaseModel):
    blockNumber: int
    callType: str
    createdContractAddressHash: str | None
    createdContractCode: str | None
    error: str | None
    fromAddressHash: str
    gas: Decimal
    gasUsed: Decimal
    id: str
    index: int
    init: str | None
    input: str
    output: str
    toAddressHash: str
    traceAddress: str
    transactionHash: str
    transactionIndex: int
    type: str
    value: Decimal


class TransactionInfo(BaseModel):
    blockNumber: int
    createdContractAddressHash: str | None
    cumulativeGasUsed: Decimal
    error: str | None
    fromAddressHash: str
    gas: Decimal
    gasPrice: Decimal
    gasUsed: Decimal
    hash: str
    id: str
    index: int
    input: str
    nonce: str
    r: Decimal
    s: Decimal
    status: str
    toAddressHash: str
    v: Decimal
    value: Decimal


def get_transaction_info(transaction_hash: str) -> TransactionInfo:
    query = (
        "{"
        f'  transaction(hash: "{transaction_hash}") {{'
        "    blockNumber"
        "    createdContractAddressHash"
        "    cumulativeGasUsed"
        "    error"
        "    fromAddressHash"
        "    gas"
        "    gasPrice"
        "    gasUsed"
        "    hash"
        "    id"
        "    index"
        "    input"
        "    nonce"
        "    r"
        "    s"
        "    status"
        "    toAddressHash"
        "    v"
        "    value"
        "  }"
        "}"
    )
    response = Client().query(query)
    return TransactionInfo(**response["transaction"])


def get_internal_transactions(
    transaction_hash: str, previous_cursor: str | None = None
) -> ([InternalTransaction], PageInfo):
    query = (
        "{"
        f'   transaction(hash: "{transaction_hash}"){{'
        f"        internalTransactions(first: 5 {generate_after_pagination_query_line(previous_cursor)}){{"
        "            edges{"
        "                node{"
        "                    blockNumber"
        "                    callType"
        "                    createdContractAddressHash"
        "                    createdContractCode"
        "                    error"
        "                    fromAddressHash"
        "                    gas"
        "                    gasUsed"
        "                    id"
        "                    index"
        "                    init"
        "                    input"
        "                    output"
        "                    toAddressHash"
        "                    traceAddress"
        "                    transactionHash"
        "                    transactionIndex"
        "                    type"
        "                    value"
        "                }"
        "            }"
        "            pageInfo{"
        "                endCursor"
        "                hasNextPage"
        "                hasPreviousPage"
        "                startCursor"
        "            }"
        "        }"
        "    }"
        "}"
    )
    response = Client().query(query)["transaction"]["internalTransactions"]
    return [InternalTransaction(**i["node"]) for i in response["edges"]], PageInfo(
        **response["pageInfo"]
    )
