from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.betjack_parser import BetJackParser
from ..scraper_utils.scraper_utils import *
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class BetJack(scrapy.Spider):
    name: str = "BetJack"
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
                        '//span[@class="PlatformHeaderNavigationItem__ItemLabelCss-sc-3mk1xi-2 jTyrEf"]',
                    )
                ),
                meta={"book": BetJack.name, "game": game.id, "sport": game.sport},
            )

    def click_show_more_buttons(self, response) -> None:
        driver = response.request.meta["driver"]
        buttons = driver.find_elements(
            By.XPATH,
            '//button[@class="EventLinePairListOfferingContent__VariantSwitcherButtonCss-sc-b5gfoo-2 xApMM"]',
        )
        scroll_to_and_click_buttons(driver, buttons)

    def parse(self, response) -> Optional[Generator]:
        self.click_show_more_buttons(response)
        sport = response.meta["sport"]
        parser = BetJackParser(response)
        yield from parser.parse(sport)
