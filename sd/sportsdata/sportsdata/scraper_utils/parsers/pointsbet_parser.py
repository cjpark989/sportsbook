from typing import Generator

from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from .base_parser import *

clean = clean_string


class PointsbetParser(BaseParser):
    """Parses Pointsbet."""

    # Annoying to parse player props

    @baseball
    def fixed_odds(response) -> Generator:
        """Parses the Fixed Odds tab."""
        labels = response.xpath("//div[@class='fddsvlq']/p//text()").getall()
        odds = response.xpath(
            "//div[@class='fdz3fpy f1yn18fe f62or3o']/div/span/button[@class='f6msbc8 f17icb0n f17icb0n f17icb0n']//text()"
        ).getall()

        team_1, team_2 = clean(labels[0]), clean(labels[1])

        spread_team_1, spread_team_1_odds = clean(odds[0]), clean(odds[1])
        spread_team_2, spread_team_2_odds = clean(odds[5]), clean(odds[6])

        over_line, over_odds = clean(odds[2]), int(clean(odds[3]))
        under_line, under_odds = clean(odds[7]), int(clean(odds[8]))

        ml_team_1_odds, ml_team_2_odds = int(clean(odds[4])), int(clean(odds[9]))
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
