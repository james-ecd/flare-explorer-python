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


class AddressInfo(BaseModel):
    contractCode: str
    fetchedCoinBalance: Decimal
    fetchedCoinBalanceBlockNumber: int
    smartContract: SmartContract


def get_address_info(address_hash: str) -> AddressInfo:
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
    return AddressInfo(**response["address"])
