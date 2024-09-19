from typing import Generator

from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from .base_parser import *

clean = clean_string

"""TODO: Deal with anti-scraping detection."""


class TipicoParser(BaseParser):
    """Parses Betway."""

    @baseball
    def money_line(response) -> Generator:
        """Parses the Money Lines."""
