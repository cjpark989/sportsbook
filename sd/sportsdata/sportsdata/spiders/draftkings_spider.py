from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.draftkings_parser import DraftKingsParser
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class DraftKings(scrapy.Spider):
    """DraftKings scraper."""

    name: str = "DraftKings"
    games: List[SportsGame] = BOOK_TO_GAME_MAP[name]

    def start_requests(self) -> Generator:
        for game in self.games:
            yield SeleniumRequest(
                url=game.url,
                callback=self.parse,
                wait_time=20,
                wait_until=EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//div[@class="sportsbook-table-header__title"]',
                    )
                ),
                screenshot=True,
                meta={"book": DraftKings.name, "game": game.id, "sport": game.sport},
            )

    def parse(self, response) -> Optional[Generator]:
        sport = response.meta["sport"]

        parser = DraftKingsParser(response)

        # set_trace()

        yield from parser.parse(sport)
