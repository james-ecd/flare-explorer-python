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


class Transaction(BaseModel):
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


def get_transaction(transaction_hash: str) -> Transaction:
    """
    Get information about a given transaction
    Args:
        transaction_hash: hash of the transaction

    Returns:
        Information about the transaction
    """
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
    return Transaction(**response["transaction"])


def get_internal_transactions(
    transaction_hash: str, previous_cursor: str | None = None
) -> ([InternalTransaction], PageInfo):
    """
    Get internal transactions for a given transaction.
    Returns in pages of size 5
    Args:
        transaction_hash: hash of the transaction
        previous_cursor: final cursor of the previous page

    Returns:
        Tuple[
            list of internal transactions,
            pagination page info
        ]
    """
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


def get_transactions_from_address(
    address_hash: str, previous_cursor: str | None = None
) -> ([Transaction], PageInfo):
    """
    Get transactions from a given address
    Args:
        address_hash: address hash
        previous_cursor: final cursor of the previous page

    Returns:
        Tuple[
            list of transactions from address,
            pagination page info
        ]
    """
    query = (
        "{"
        f'   address(hash: "{address_hash}"){{'
        f"        transactions(first: 5 {generate_after_pagination_query_line(previous_cursor)}) {{"
        "            edges {"
        "                node {"
        "                    blockNumber"
        "                    createdContractAddressHash"
        "                    cumulativeGasUsed"
        "                    error"
        "                    fromAddressHash"
        "                    gas"
        "                    gasPrice"
        "                    gasUsed"
        "                    hash"
        "                    id"
        "                    index"
        "                    input"
        "                    nonce"
        "                    r"
        "                    s"
        "                    status"
        "                    toAddressHash"
        "                    v"
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
    response = Client().query(query)["address"]["transactions"]
    return [Transaction(**i["node"]) for i in response["edges"]], PageInfo(
        **response["pageInfo"]
    )
