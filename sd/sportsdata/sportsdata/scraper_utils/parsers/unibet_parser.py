from typing import Generator

from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from .base_parser import *

clean = clean_string


class UnibetParser(BaseParser):
    """Parses Unibet."""

    @baseball
    def most_popular(response) -> Generator:
        """Parses the Most Popular Area."""
        data = response.xpath(
            "//div[@class='CollapsibleContainer__CollapsibleContent-sc-14bpk80-3 fQoDuY']//li//div[@data-touch-feedback='true']//text()"
        ).getall()
        team_1, team_2 = clean(data[0]), clean(data[2])

        ml_team_1_odds, ml_team_2_odds = int(clean(data[1])), int(clean(data[3]))

        spread_team_1, spread_team_1_odds = clean(data[8]), int(clean(data[9]))
        spread_team_2, spread_team_2_odds = clean(data[5]), int(clean(data[6]))

        over_line, over_odds = clean(f"{data[10]} {data[11]}"), int(clean(data[12]))
        under_line, under_odds = clean(f"{data[13]} {data[14]}"), int(clean(data[15]))

        meta = get_meta(response)

        """Spread Odds"""
        yield spread_odds(
            meta=meta, team=team_1, spread=spread_team_1, odds=spread_team_1_odds
        )

        yield spread_odds(
            meta=meta, team=team_2, spread=spread_team_2, odds=spread_team_2_odds
        )

        """Over/Under Odds"""
        yield over_under_odds(
            meta=meta,
            team_1=team_1,
            team_2=team_2,
            line=over_line,
            odds=over_odds,
        )

        yield over_under_odds(
            meta=meta,
            team_1=team_1,
            team_2=team_2,
            line=under_line,
            odds=under_odds,
        )

        """Moneyline Odds"""
        yield moneyline_odds(
            meta=meta,
            team=team_1,
            odds=ml_team_1_odds,
        )

        yield moneyline_odds(
            meta=meta,
            team=team_2,
            odds=ml_team_2_odds,
        )
