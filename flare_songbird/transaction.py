from decimal import Decimal

from pydantic import BaseModel

from flare_songbird.api import Api


class TransactionResponse(BaseModel):
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


def get_transaction_info(hash: str) -> TransactionResponse:
    query = (
        "{"
        f'  transaction(hash: "{hash}") {{'
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
    response = Api().make_request(query)
    return TransactionResponse(**response["data"]["transaction"])
