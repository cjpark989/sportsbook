from typing import Generator

from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from .base_parser import *

clean = clean_string


class DraftKingsParser(BaseParser):
    """Parses DraftKings."""

    @baseball
    def popular(response) -> Generator:
        """Parses the popular tab.

        TODO: We assume that popular will always have run line, total, and moneyline.
            Must verify that this is actually the case.
        """
        labels = (
            response.xpath(
                "//table[@class='sportsbook-table']//div[@class='sportsbook-table-header__title']/span[text()='Game']"
            )[0]
            .xpath(
                "../../../../../../table/tbody/tr/th//div[@class='event-cell__name-text']//text()"
            )
            .getall()
        )
        odds = (
            response.xpath(
                "//table[@class='sportsbook-table']//div[@class='sportsbook-table-header__title']/span[text()='Game']"
            )[0]
            .xpath("../../../../../../table/tbody/tr/td//text()")
            .getall()
        )

        team_1, team_2 = clean(labels[0]), clean(labels[1])

        spread_team_1, spread_team_1_odds = clean(odds[0]), int(clean(odds[1]))
        spread_team_2, spread_team_2_odds = clean(odds[7]), int(clean(odds[8]))

        over_line, over_odds = clean(f"{odds[2]} {odds[4]}"), int(clean(odds[5]))
        under_line, under_odds = clean(f"{odds[9]} {odds[11]}"), int(clean(odds[12]))

        ml_team_1_odds, ml_team_2_odds = int(clean(odds[6])), int(clean(odds[13]))

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

    @football
    def football_popular(response) -> Generator:
        """Parses the popular tab from"""
        labels = (
            response.xpath(
                "//table[@class='sportsbook-table']//div[@class='sportsbook-table-header__title']/span[text()='Game']"
            )[0]
            .xpath(
                "../../../../../../table/tbody/tr/th//div[@class='event-cell__name-text']//text()"
            )
            .getall()
        )
        odds = (
            response.xpath(
                "//table[@class='sportsbook-table']//div[@class='sportsbook-table-header__title']/span[text()='Game']"
            )[0]
            .xpath("../../../../../../table/tbody/tr/td//text()")
            .getall()
        )

        team_1, team_2 = clean(labels[0]), clean(labels[1])

        spread_team_1, spread_team_1_odds = clean(odds[0]), int(clean(odds[1]))
        spread_team_2, spread_team_2_odds = clean(odds[7]), int(clean(odds[8]))

        over_line, over_odds = clean(f"{odds[2]} {odds[4]}"), int(clean(odds[5]))
        under_line, under_odds = clean(f"{odds[9]} {odds[11]}"), int(clean(odds[12]))

        ml_team_1_odds, ml_team_2_odds = int(clean(odds[6])), int(clean(odds[13]))

        meta = get_meta(response)

        # Spread Odds.
        yield spread_odds(
            meta=meta,
            market_description=f"{float(spread_team_1)} Spread",
            odds=[spread_team_1_odds, spread_team_2_odds],
            plays=[f"{team_1} {spread_team_1}", f"{team_2} {spread_team_2}"],
        )

        # Over/Under Odds.
        yield over_under_odds(
            meta=meta,
            market_description="Total",
            odds=[over_odds, under_odds],
            plays=[f"{team_1} {over_line}", f"{team_2} {under_line}"],
        )

        # Moneyline Odds.
        yield moneyline_odds(
            meta=meta,
            market_description="Moneyline",
            odds=[ml_team_1_odds, ml_team_2_odds],
            plays=[team_1, team_2],
        )
