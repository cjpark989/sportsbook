from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.bet365_parser import Bet365Parser
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class Bet365(scrapy.Spider):
    """Bet365 scraper."""

    """
    Bet365 has anti-bot detection.
    """

    name: str = "Bet365"
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
                        '//div[@class="hm-MainHeaderCentreWide_Link hm-HeaderMenuItem hm-HeaderMenuItem_LinkSelected hm-HeaderMenuItem_LinkSelected-underscore "]',
                    )
                ),
                meta={"book": Bet365.name, "game": game.id, "sport": game.sport},
            )

    def parse(self, response) -> Optional[Generator]:
        sport = response.meta["sport"]
        parser = Bet365Parser(response)
        yield from parser.parse(sport)
