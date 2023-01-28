from decimal import Decimal

from pydantic import BaseModel

from flare_explorer.gql_client import Client


class SmartContract(BaseModel):
    abi: str
    addressHash: str
    compilerVersion: str
    contractSourceCode: str
    name: str
    optimization: bool


class Address(BaseModel):
    contractCode: str | None
    fetchedCoinBalance: Decimal
    fetchedCoinBalanceBlockNumber: int
    smartContract: SmartContract | None


def get_address(address_hash: str) -> Address:
    """
    Get information about a given address
    Args:
        address_hash: hash of the address

    Returns:
        Information about the address
    """
    query = (
        "{"
        f'   address(hash: "{address_hash}") {{'
        "        contractCode"
        "        fetchedCoinBalance"
        "        fetchedCoinBalanceBlockNumber"
        "        smartContract {"
        "            abi"
        "            addressHash"
        "            compilerVersion"
        "            contractSourceCode"
        "            name"
        "            optimization"
        "        }"
        "    }"
        "}"
    )
    response = Client().query(query)
    return Address(**response["address"])
