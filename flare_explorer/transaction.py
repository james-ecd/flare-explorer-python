from decimal import Decimal
from typing import List

from pydantic import BaseModel

from flare_explorer.gql_client import Client


class InternalTransaction(BaseModel):
    input: str
    output: str
    toAddressHash: str
    fromAddressHash: str

    @classmethod
    def serialize_internal_transactions_from_info_response(
        cls, internal_transactions: dict
    ) -> List["InternalTransaction"]:
        return (
            [cls(**i["node"]) for i in internal_transactions["edges"]]
            if internal_transactions
            else []
        )


class TransactionInfoResponse(BaseModel):
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
    internalTransactions: List[InternalTransaction]


def get_transaction_info(
    transaction_hash: str, num_internal_transactions: int = 10
) -> TransactionInfoResponse:
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
        f"   internalTransactions(first:{num_internal_transactions}){{"
        "      edges {"
        "        node {"
        "          input"
        "          output"
        "          toAddressHash"
        "          fromAddressHash"
        "        }"
        "      }"
        "    }"
        "  }"
        "}"
    )
    response = Client().query(query)
    response["transaction"][
        "internalTransactions"
    ] = InternalTransaction.serialize_internal_transactions_from_info_response(
        response["transaction"]["internalTransactions"]
    )
    return TransactionInfoResponse(**response["transaction"])
