import json
from typing import Generator

from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from .base_parser import *

clean = clean_string


class BetJackParser(BaseParser):
    """Parses BetJack."""

    @tennis
    def tennis_game_lines(response) -> Generator:
        popular_odds = response.xpath("//div//button//div//text()").getall()

        player_one_ml, odds_one_ml = clean(popular_odds[0]), clean(popular_odds[1])
        player_two_ml, odds_two_ml = clean(popular_odds[2]), clean(popular_odds[3])

        meta = get_meta(response)

        yield ScrapedOdds(
            time_ns=time_ns(),
            book=meta.book,
            sport=meta.sport,
            game_id=meta.id,
            market_description=f"Game Outcome (Moneyline)",
            market_id=1,
            plays=json.dumps([player_one_ml, player_two_ml]),
            odds=json.dumps([odds_one_ml, odds_two_ml]),
        )

    @baseball
    def game_lines(response) -> Generator:
        """Parses the Game Lines."""
        # response = click_tab_you_are_responsible_for(response)

        popular_odds = response.xpath("//div//button//div//text()").getall()

        team_one_ml, odds_one_ml = clean(popular_odds[0]), clean(popular_odds[1])
        team_two_ml, odds_two_ml = clean(popular_odds[2]), clean(popular_odds[3])

        ou_one, ou_line_one, ou_line_odds_one = (
            clean(popular_odds[4]),
            clean(popular_odds[5]),
            clean(popular_odds[6]),
        )
        ou_two, ou_line_two, ou_line_odds_two = (
            clean(popular_odds[7]),
            clean(popular_odds[8]),
            clean(popular_odds[9]),
        )

        spread_team_one, spread_line_one, spread_odds_one = (
            clean(popular_odds[10]),
            clean(popular_odds[11]),
            clean(popular_odds[12]),
        )
        spread_team_two, spread_line_two, spread_odds_two = (
            clean(popular_odds[13]),
            clean(popular_odds[14]),
            clean(popular_odds[15]),
        )

        """Moneyline Odds"""
        meta = get_meta(response)

        yield moneyline_odds(
            meta=meta,
            team=team_one_ml,
            odds=odds_one_ml,
        )

        yield moneyline_odds(
            meta=meta,
            team=team_two_ml,
            odds=odds_two_ml,
        )

        """Over/Under Odds"""
        yield over_under_odds(
            meta=meta,
            team_1=team_one_ml,
            team_2=team_two_ml,
            line=f"{ou_one} {ou_line_one}",
            odds=ou_line_odds_one,
        )

        yield over_under_odds(
            meta=meta,
            team_1=team_one_ml,
            team_2=team_two_ml,
            line=f"{ou_two} {ou_line_two}",
            odds=ou_line_odds_two,
        )

        """Spread odds"""
        yield spread_odds(
            meta=meta,
            team=spread_team_one,
            spread=spread_line_one,
            odds=spread_odds_one,
        )

        yield spread_odds(
            meta=meta,
            team=spread_team_two,
            spread=spread_line_two,
            odds=spread_odds_two,
        )
