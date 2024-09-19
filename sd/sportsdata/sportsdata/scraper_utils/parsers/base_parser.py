"""Generic parser meant to provide odds from a HtmlResponse provided by a spider."""
from collections import defaultdict
from dataclasses import dataclass
from typing import Generator

PARSER_FUNCTIONS = defaultdict(lambda: defaultdict(list))


"""Decorators to register a function that parses a particular sport."""


def baseball(func):
    return register(func, "baseball")


def football(func):
    return register(func, "football")


def tennis(func):
    return register(func, "tennis")


def register(func, sport_name: str):
    class_name: str = func.__qualname__.split(".")[0]
    PARSER_FUNCTIONS[class_name][sport_name].append(func)
    return staticmethod(func)


@dataclass
class GameMetaInfo:
    book: str
    """Name of the book."""
    sport: str
    """Name of the sport."""
    id: str
    """Game identifier."""
    source_url: str
    """Source URL of the game."""


def get_meta(response) -> GameMetaInfo:
    return GameMetaInfo(
        response.request.meta["book"],
        response.request.meta["sport"],
        response.request.meta["game"],
        response.url,
    )

<<<<<<< HEAD
=======

>>>>>>> 353dfa48421b127d1562814c365fc70c5e872f90
class BaseParser:
    """Base parser."""

    def __init__(self, response) -> None:
        self.response = response

    def parse(self, sport_name: str) -> Generator:
        """Produces a list of items from the given parser."""
        methods = PARSER_FUNCTIONS[self.__class__.__name__][sport_name]

        for method in methods:
            yield from method(self.response)
