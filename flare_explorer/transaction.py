from decimal import Decimal
from typing import List

from pydantic import BaseModel, validator

from flare_explorer.api import Api


class InternalTransaction(BaseModel):
    id: str
    transactionHash: str

    @classmethod
    def transform_internal_transaction_graph_to_nodes(
        cls, graph: dict
    ) -> List["InternalTransaction"]:
        return [cls(**i["node"]) for i in graph["edges"]] if graph else []


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
    _extract_internal_transactions = validator(
        "internalTransactions", pre=True, allow_reuse=True
    )(InternalTransaction.transform_internal_transaction_graph_to_nodes)


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
        "          id"
        "          transactionHash"
        "        }"
        "      }"
        "    }"
        "  }"
        "}"
    )
    response = Api().make_query_request(query)
    return TransactionInfoResponse(**response["transaction"])
