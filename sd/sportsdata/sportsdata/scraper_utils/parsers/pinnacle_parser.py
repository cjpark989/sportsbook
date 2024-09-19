from typing import Generator

import json
from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from ..statistics_utils import *
from .base_parser import *

clean = clean_string

"""TODO: Wait on cookies."""

class PinnacleParser(BaseParser):
    """Parses Bet365."""

    @baseball
    def game_lines(response) -> Generator:
      """Parses the Game Lines."""

    @football
    def game_lines(response) -> Generator:
      meta = get_meta(response)

      # Parse moneyline teams
      teams = response.xpath('//span[text()="Money Line – Game"]/../..//span[@class="style_label__3BBxD"]//text()').getall()

      # Parse moneyline
      moneyline_odds = response.xpath('//span[text()="Money Line – Game"]/../..//span[@class="style_price__3Haa9"]//text()').getall()
      moneyline_odds = [decimal_odds_to_american_odds(float(x)) for x in moneyline_odds]

      yield ScrapedOdds(
        time_ns=time_ns(),
        book=meta.book,
        sport=meta.sport,
        game_description=meta.id,
        market_description=f'Moneyline',
        plays=json.dumps([teams[0], teams[1]]),
        odds=json.dumps([moneyline_odds[0], moneyline_odds[1]]),
      )
