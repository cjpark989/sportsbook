from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.unibet_parser import UnibetParser
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class Unibet(scrapy.Spider):
    """Unibet scraper."""

    name: str = "Unibet"
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
                        '//header[@class="CollapsibleContainer__HeaderWrapper-sc-14bpk80-1 ivA-DKq"]',
                    )
                ),
                screenshot=True,
                meta={"book": Unibet.name, "game": game.id, "sport": game.sport},
            )

    def parse(self, response) -> Optional[Generator]:
        sport = response.meta["sport"]

        parser = UnibetParser(response)

        set_trace()

        yield from parser.parse(sport)
