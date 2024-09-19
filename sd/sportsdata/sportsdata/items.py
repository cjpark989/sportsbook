"""
Define here the models for your scraped items

See documentation in:
https://docs.scrapy.org/en/latest/topics/items.html
"""

import os
import sys
from typing import List

import django
import scrapy
from scrapy_djangoitem import DjangoItem

from .scraper_utils.parsers.base_parser import GameMetaInfo
from .scraper_utils.utils import *

sys.path.append("../ui")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings")
django.setup()

from odds.models import OddsItem


class ScrapedOdds(DjangoItem):
    django_model = OddsItem

    """
    # time_ns (Unix timestamp)
    time_ns = scrapy.Field()

    # Sportsbook (e.g., BetMGM, DK, etc)
    book = scrapy.Field()

    # Sport that the OddsItem corresponds to.
    sport = scrapy.Field()

    # Unique ID to represent a market. One "game" corresponds to a single ID.
    game_id = scrapy.Field()

    # Market category (e.g., totals, outright, etc)
    odds_description = scrapy.Field()

    # Signed integer
    odds = scrapy.Field()
    """


def spread_odds(
    meta: GameMetaInfo,
    market_description: str,
    odds: List[int],
    plays: List[str],
) -> ScrapedOdds:
    """Produces an spreads odds item.

    TODO: Perform validation here.

    Args:
        meta: Meta information on the game.
        market_description: Description of the market.
        odds: Odds of each play.
        plays: Spread plays.

    Returns:
        Odds item representing a spread market.
    """
    return ScrapedOdds(
        time_ns=time_ns(),
        book=meta.book,
        sport=meta.sport,
        game_description=meta.id,
        market_description=market_description,
        odds=str(odds),
        plays=str(plays),
        source_url=meta.source_url,
    )


def over_under_odds(
    meta: GameMetaInfo,
    market_description: str,
    odds: List[int],
    plays: List[str],
) -> ScrapedOdds:
    """Produces an over/under odds item.

    TODO: Perform validation here.

    Args:
        meta: Meta information on the game.
        market_description: Description of the market.
        odds: Odds of each play.
        plays: Over/under plays.

    Returns:
        Odds item representing an over/under market.
    """
    return ScrapedOdds(
        time_ns=time_ns(),
        book=meta.book,
        sport=meta.sport,
        game_description=meta.id,
        market_description=market_description,
        odds=str(odds),
        plays=str(plays),
        source_url=meta.source_url,
    )


def moneyline_odds(
    meta: GameMetaInfo,
    market_description: str,
    odds: List[int],
    plays: List[str],
) -> ScrapedOdds:
    """Produces a moneyline odds item.

    TODO: Perform validation here.

    Args:
        meta: Meta information on the game.
        market_description: Description of the market.
        odds: Odds of each play.
        plays: Moneyline plays.

    Returns:
        Odds item representing a moneyline market.
    """

    return ScrapedOdds(
        time_ns=time_ns(),
        book=meta.book,
        sport=meta.sport,
        game_description=meta.id,
        market_description=market_description,
        odds=str(odds),
        plays=str(plays),
        source_url=meta.source_url,
    )
