from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.betway_parser import BetwayParser
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class Betway(scrapy.Spider):
    """Betway scraper."""

    name: str = "Betway"
    games: List[SportsGame] = BOOK_TO_GAME_MAP[name]

    def start_requests(self) -> Generator:
        for game in self.games:
            # TODO: Add wait_until flag.
            yield SeleniumRequest(
                url=game.url,
                callback=self.parse,
                wait_time=20,
                wait_until=EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//div[@class="cashOutIcon icon-cashout"]',
                    )
                ),
                screenshot=True,
                meta={"book": Betway.name, "game": game.id, "sport": game.sport},
            )

    def parse(self, response) -> Optional[Generator]:
        sport = response.meta["sport"]
        parser = BetwayParser(response)
        yield from parser.parse(sport)
