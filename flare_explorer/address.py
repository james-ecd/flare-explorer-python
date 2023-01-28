from decimal import Decimal

from pydantic import BaseModel

from flare_explorer.exceptions import QueryComplexityLimit
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


def get_addresses(address_hashes: [str]) -> [Address]:
    """
    Get multiple addresses in one call.
    API complexity limit is 15 addresses at once
    Args:
        address_hashes: list of address hashes

    Returns:
        List of address objects

    Raises:
        QueryComplexityLimit: if address_hashes is > 15 hashes
    """
    if len(address_hashes) > 15:
        raise QueryComplexityLimit("Limit of 15 addresses breached")
    query_args = ",".join([f'"{i}"' for i in address_hashes])
    query = (
        "{"
        f"   addresses(hashes: [{query_args}]) {{"
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
    return [Address(**i) for i in response["addresses"]]
