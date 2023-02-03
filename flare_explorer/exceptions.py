class BaseFlareExplorerException(Exception):
    """Base exception for errors raised in the Flare explorer package"""


class FlareExplorerQueryError(BaseFlareExplorerException):
    """An error was returned by flare explorer with the given query"""


class QueryComplexityLimit(BaseFlareExplorerException):
    """Too many inputs to flare explorer, api will return complexity error"""
