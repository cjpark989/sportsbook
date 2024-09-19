from typing import Generator

from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from .base_parser import *

clean = clean_string

"""TODO: Deal with anti-scraping detection."""


class FanDuelParser(BaseParser):
    """Parses FanDuel."""

    @baseball
    def game_lines(response) -> Generator:
        """Parses the Game Lines."""
