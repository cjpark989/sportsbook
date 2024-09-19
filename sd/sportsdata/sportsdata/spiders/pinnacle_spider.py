from typing import Generator, List, Optional

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..scraper_utils.market_utils import *
from ..scraper_utils.parsers.pinnacle_parser import PinnacleParser
from ..scraper_utils.string_utils import *
from ..scraper_utils.scraper_utils import *
from ..scraper_utils.utils import *


class Pinnacle(scrapy.Spider):
    """DraftKings scraper."""

    name: str = "Pinnacle"
    games: List[SportsGame] = BOOK_TO_GAME_MAP[name]

    def start_requests(self) -> Generator:
      for game in self.games:
          yield SeleniumRequest(
              url=game.url,
              callback=self.parse,
              wait_time=25,
              wait_until=EC.presence_of_element_located( ( By.XPATH, '//div[@class="style_desktop_logo__BYlm6"]')),
              meta={"book": Pinnacle.name, "game": game.id, "sport": game.sport},
          )

    def click_show_more_buttons(self, response) -> None:
      driver = response.request.meta['driver']
      buttons = driver.find_elements(By.XPATH, '//i[@class="icon-chevron-right-sml style_arrow__1pSnm"]')
      scroll_to_and_click_buttons(driver, buttons)

    def parse(self, response) -> Optional[Generator]:
        self.click_show_more_buttons(response)
        sport = response.meta["sport"]
        parser = PinnacleParser(response)
        yield from parser.parse(sport)
