from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.betmgm_parser import BetMGMParser
from ..scraper_utils.scraper_utils import *
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class BetMGM(scrapy.Spider):
    """BetMGM scraper."""

    name: str = "BetMGM"
    games: List[SportsGame] = BOOK_TO_GAME_MAP["BetMGM"]

    def start_requests(self) -> Generator:
        for game in self.games:
            yield SeleniumRequest(
                url=game.url,
                callback=self.parse,
                wait_time=20,
                wait_until=EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".option-group-name-info-name.ng-star-inserted")
                ),
                screenshot=True,
                meta={"book": BetMGM.name, "game": game.id, "sport": game.sport},
            )

    def parse(self, response) -> Optional[Generator]:
        self.scroll_to_bottom(response)
        self.click_show_more_buttons(response)
        sport = response.meta["sport"]
        parser = BetMGMParser(response)
        yield from parser.parse(sport)

    def click_show_more_buttons(self, response) -> None:
        """Click all of the "Show more" buttons so that we can scrape all of the odds on the page."""
        driver = response.request.meta["driver"]
        buttons = response.request.meta["driver"].find_elements(
            By.XPATH, '//div[@class="show-more-less-button ng-star-inserted"]'
        )
        scroll_to_and_click_buttons(driver, buttons)
        response = scrapy.http.response.html.HtmlResponse(
            url=response.meta["driver"].current_url,
            body=response.meta["driver"].page_source,
            encoding="utf-8",
        )

    def scroll_to_bottom(self, response) -> None:
        """Scroll to the bottom fo the page so that the Javascript renders all of the odds on the page."""
