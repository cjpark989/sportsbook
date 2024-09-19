from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.fanduel_parser import FanDuelParser
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class FanDuel(scrapy.Spider):
    """FanDuel scraper."""

    name: str = "FanDuel"
    games: List[SportsGame] = BOOK_TO_GAME_MAP[name]

    def start_requests(self) -> Generator:
        for game in self.games:
            # TODO: Add wait_until flag.
            yield SeleniumRequest(
                url=game.url,
                callback=self.parse,
                wait_time=20,
                screenshot=True,
                meta={"book": FanDuel.name, "game": game.id, "sport": game.sport},
            )

    def parse(self, response) -> Optional[Generator]:
        sport = response.meta["sport"]
        parser = FanDuelParser(response)
        yield from parser.parse(sport)
