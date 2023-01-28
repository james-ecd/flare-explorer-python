# Flare explorer python
<a href="https://pypi.org/project/flare-explorer-python" target="_blank"><img src="https://img.shields.io/pypi/v/flare-explorer-python?color=%2334D058&label=pypi%20package" alt="Package version"></a>
[![Linting and tests](https://github.com/james-ecd/flare-explorer-python/actions/workflows/tests-and-linting.yml/badge.svg?branch=main)](https://github.com/james-ecd/flare-explorer-python/actions/workflows/tests-and-linting.yml)
[![codecov](https://codecov.io/gh/james-ecd/flare-explorer-python/branch/main/graph/badge.svg?token=XOBC0UK00V)](https://codecov.io/gh/james-ecd/flare-explorer-python)
<a href="https://pypi.org/project/flare-explorer-python" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/flare-explorer-python.svg?color=%2334D058" alt="Supported Python versions">
</a>
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight library that works as a connector to the [Flare explorer api](https://flare-explorer.flare.network/graphiql)

If you came here looking for the flare network, then go [here](https://flare.network/). If you want to query flares blockchain using python then stick around.

## Installation
flare-explorer-python is available on PYPI. Install with pip or poetry:

```
pip install flare-explorer-python
```
```
poetry add flare-explorer-python
```

## Usage
### Transactions
``` python
from flare_explorer.transaction import (
    get_internal_transactions,
    get_transaction,
    get_transactions_from_address,
)

transaction = get_transaction("transaction_hash")

internal_transactions, page_info = get_internal_transactions(
    "transaction_hash",
    previous_cursor="previous_page_last_cursor"
)

transactions, page_info = get_transactions_from_address(
    "address_hash",
    previous_cursor="previous_page_last_cursor"
)
```

### Addresses
``` python
from flare_explorer.address import get_address, get_addresses

address = get_address(
    "address_hash",
)

addresses = get_addresses(
    [
        "address_hash_1",
        "address_hash_2",
    ]
)
```

### Blocks
``` python
from flare_explorer.block import get_block

block = get_block(4463469)
```

### Token transfers
``` python
from flare_explorer.token_transfers import get_token_transfers

token_transfers, page_info = get_token_transfers(
    "token_contract_address_hash",
    previous_cursor="previous_page_last_cursor"
)
```

## Upcoming features
- asyncio support
- websocket support
- fast mode (no pydantic serialization)

## Testing / Contributing
Any contributions or issue raising is welcomed. If you wish to contribute then:
1. fork/clone this repo
2. make changes on a branch taken from main
3. sumbit a pull request against main

Pull requests will be blocked from merging automatically if:
- less than 100% coverage
- there are failing tests
- linting rules have been violated.
