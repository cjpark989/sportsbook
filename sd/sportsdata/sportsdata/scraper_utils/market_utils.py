"""Market utilities."""
from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import yaml

BOOK_TO_GAME_MAP: Dict[str, List[SportsGame]] = defaultdict(list)
"""Map used to store games by their respective sports book."""
MARKET_DATA_PATH = Path(__file__).parent.parent.resolve() / "sports_markets"
"""Path to find all of the market data files."""

@dataclass
class SportsGame:
    """Sports Game information."""

    sport: str
    book: str
    id: str
    url: str

    def __post_init__(self) -> None:
        """Whenever a SportsGame is defined, add it to this map."""
        BOOK_TO_GAME_MAP[self.book].append(self)


"""At import time, find all market data, parse, and store."""
for _, _, file_names in os.walk(MARKET_DATA_PATH):
    for file_name in file_names:
        if file_name.endswith(".yaml"):
            with open(str(MARKET_DATA_PATH / file_name), "r") as file:
                market_data = yaml.full_load(file)
                if market_data:
                    book = market_data.pop("book")
                    for sport, games in market_data.items():
                        for game in games:
                            SportsGame(
                                sport=sport,
                                book=book,
                                id=game["id"],
                                url=game["url"],
                            )
