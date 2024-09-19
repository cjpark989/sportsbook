from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.pointsbet_parser import PointsbetParser
from ..scraper_utils.scraper_utils import *
from ..scraper_utils.string_utils import *
from ..scraper_utils.utils import *


class Pointsbet(scrapy.Spider):
    """Pointsbet scraper."""

    name: str = "Pointsbet"
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
                        '//button[@data-test="sportsEventMainContent0TabButton"]',
                    )
                ),
                screenshot=True,
                meta={"book": Pointsbet.name, "game": game.id, "sport": game.sport},
            )

    def expand_tabs(self, response) -> None:
        # Expand twice. Once to click the dropdowns and a second time to click the nested dropdowns.
        buttons_xpath = '//div[@identifier="sports_default_event-fixed"]//button[@name="accordionButton" and @aria-expanded="false"]'
        driver = response.request.meta["driver"]
        scroll_to_and_click_buttons(
            driver, driver.find_elements(By.XPATH, buttons_xpath)
        )
        scroll_to_and_click_buttons(
            driver, driver.find_elements(By.XPATH, buttons_xpath)
        )  # intentionally duplicated.

    def parse(self, response) -> Optional[Generator]:
        sport = response.meta["sport"]
        self.expand_tabs(response)

        response = scrapy.http.response.html.HtmlResponse(
            url=response.meta["driver"].current_url,
            body=response.meta["driver"].page_source,
            encoding="utf-8",
            request=response.request,
        )

        # annoying to parse rest
        parser = PointsbetParser(response)
        yield from parser.parse(sport)
