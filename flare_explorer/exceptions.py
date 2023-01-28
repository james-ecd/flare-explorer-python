class BaseFlareExplorerException(Exception):
    """Base exception for errors raised in the Flare explorer package"""


class FlareExplorerNoneBadResponseCode(BaseFlareExplorerException):
    """A None 200 status code was given from the flare explorer api"""


class FlareExplorerQueryError(BaseFlareExplorerException):
    """An error was returned by flare explorer with the given query"""


class QueryComplexityLimit(BaseFlareExplorerException):
    """Too many inputs to flare explorer, api will return complexity error"""
