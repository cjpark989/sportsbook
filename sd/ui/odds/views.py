import json
import math
import statistics
from dataclasses import dataclass

from django.http import HttpResponse
from django.shortcuts import render

from .models import OddsItem

# Create your views here.
INF = math.inf


@dataclass
class Outcome:
    play: str

    # (sportsbook, url, odd)
    book_odds: list[tuple[str, str, int]]

    best_odd: int
    median: float
    mean: float
    std: float


@dataclass
class MarketMeta:
    description: str
    outcomes: list[Outcome]


def index(request):
    latest_odds = OddsItem.objects.order_by("-time_ns")[:5]
    odds_list = [str(x) for x in latest_odds]
    return render(request, "odds/index.html", {"latest_odds": odds_list})


def game(request, game_description: str):
    ## TODO: Query the database for every odds with matching game_id and display it in a table.

    for _ in range(100):
        odds_items = OddsItem.objects.filter(game_description=game_description)
        distinct_markets = sorted(
            list(
                set(odds_items.values_list("market_description", flat=True).distinct())
            )
        )
        market_metadata = []

        for market_name in distinct_markets:
            market_qs = odds_items.filter(market_description=market_name)
            parsed_plays = json.loads(market_qs[0].plays.replace("'", '"'))

            outcomes = [
                Outcome(
                    play=parsed_plays[idx],
                    book_odds=[],
                    best_odd=-INF,
                    mean=-INF,
                    median=-INF,
                    std=-INF,
                )
                for idx in range(len(parsed_plays))
            ]

            for odds_item in market_qs:
                parsed_odds = [
                    int(odd) for odd in json.loads(odds_item.odds.replace("'", '"'))
                ]
                parsed_odds = [
                    str(odd) if odd < 0 else f"+{odd}" for odd in parsed_odds
                ]

                for idx, odd in enumerate(parsed_odds):
                    outcomes[idx].book_odds.append(
                        (odds_item.book, odds_item.source_url, odd)
                    )

            for outcome in outcomes:
                all_odds = [int(odd) for sb, url, odd in outcome.book_odds]
                outcome.best_odd = max(all_odds)
                outcome.median = statistics.median(all_odds)
                outcome.std = 0 if len(all_odds) <= 1 else statistics.stdev(all_odds)
                outcome.mean = statistics.mean(all_odds)

            market_metadata.append(
                MarketMeta(
                    description=market_qs[0].market_description,
                    outcomes=outcomes,
                )
            )

        game_description = game_description if len(odds_items) != 0 else None

        return render(
            request,
            "odds/game.html",
            {
                "game_description": game_description,
                "odds_items": odds_items,
                "market_metadata": market_metadata,
            },
        )
