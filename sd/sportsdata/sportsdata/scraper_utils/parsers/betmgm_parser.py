from typing import Generator

from ...items import *
from ..market_utils import *
from ..string_utils import *
from ..utils import *
from .base_parser import *

clean = clean_string


class BetMGMParser(BaseParser):
    """Parses BetMGM."""

    @baseball
    def parse_game_lines(response) -> Generator:
        """Parses the game lines."""
        labels = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[text()="Game Lines"]'
            )[0]
            .xpath(
                '../../../../../../ms-period-option-group[@class="ng-star-inserted"]/ms-six-pack-option-group/div//span/text()'
            )
            .getall()
        )
        odds = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[text()="Game Lines"]'
            )[0]
            .xpath(
                '../../../../../../ms-period-option-group[@class="ng-star-inserted"]/ms-six-pack-option-group//ms-event-pick//text()'
            )
            .getall()
        )

        team_1, team_2 = labels[-2], labels[-1]
        spread_team_1, spread_team_1_odds = clean(odds[0]), int(clean(odds[1]))
        over_line, over_odds = clean(odds[2]), int(clean(odds[3]))
        ml_team_1_odds = clean(odds[4])
        spread_team_2, spread_team_2_odds = clean(odds[5]), int(clean(odds[6]))
        under_line, under_odds = clean(odds[7]), int(clean(odds[8]))
        ml_team_2_odds = clean(odds[9])

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

    @baseball
    def parse_winning_margins(response) -> Generator:
        margins = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[text()="Winning Margin"]'
            )[0]
            .xpath(
                '../../../../../../ms-regular-group[@class="ng-star-inserted"]//ms-option[@class="option ng-star-inserted"]/div[@class="name ng-star-inserted"]/text()'
            )
            .getall()
        )
        odds = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[text()="Winning Margin"]'
            )[0]
            .xpath(
                '../../../../../../ms-regular-group[@class="ng-star-inserted"]//ms-option[@class="option ng-star-inserted"]/ms-event-pick//text()'
            )
            .getall()
        )

        for margin, odd in zip(margins, odds):
            yield OddsItem(
                time_ns=time_ns(),
                book="BetMGM",
                sport="baseball",
                game_id=response.meta["game"],
                odds_description=clean(margin),
                odds=int(odd),
            )

    @baseball
    def parse_odd_even_total_score(response) -> Generator:
        parities = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[text()="Will the final score be odd or even?"]'
            )[0]
            .xpath(
                '../../../../../../ms-regular-group//div[@class="name ng-star-inserted"]/text()'
            )
            .getall()
        )
        odds = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[text()="Will the final score be odd or even?"]'
            )[0]
            .xpath(
                '../../../../../../ms-regular-group//ms-event-pick/div[@class="option-indicator"]//text()'
            )
            .getall()
        )

        for parity, odd in zip(parities, odds):
            yield OddsItem(
                time_ns=time_ns(),
                book="BetMGM",
                sport="baseball",
                game_id=response.meta["game"],
                odds_description=f"Will the final score be {parity}?",
                odds=int(odd),
            )

    @baseball
    def parse_total_runs(response) -> Generator:
        # TODO: Sometimes, the text says "Total runs" rather than "runs"
        odds_description = response.xpath(
            '//div[@class="option-group-name clickable"]/div/div/div/span[starts-with(text(), "How many runs will the")]//text()'
        ).getall()[0]
        ou_ordering = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[starts-with(text(), "How many runs will the")]'
            )[0]
            .xpath(
                '../../../../../..//ms-over-under-option-group//div[@class="option-group-header"]//text()'
            )
            .getall()
        )
        lines = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[starts-with(text(), "How many runs will the")]'
            )[0]
            .xpath(
                '../../../../../..//ms-over-under-option-group//div[@class="attribute-key ng-star-inserted"]//text()'
            )
            .getall()
        )
        odds = (
            response.xpath(
                '//div[@class="option-group-name clickable"]/div/div/div/span[starts-with(text(), "How many runs will the")]'
            )[0]
            .xpath(
                '../../../../../..//ms-over-under-option-group//ms-option[@class="option ng-star-inserted"]//div[@class="value option-value ng-star-inserted"]/text()'
            )
            .getall()
        )

        for idx, odd in enumerate(odds):
            ordering_idx = 0 if idx % 2 == 0 else 1

            yield OddsItem(
                time_ns=time_ns(),
                book="BetMGM",
                sport="baseball",
                game_id=response.meta["game"],
                odds_description=f"{clean(odds_description)} ({clean(ou_ordering[ordering_idx])} {clean(lines[idx // 2])})",
                odds=int(clean(odd)),
            )

    @baseball
    def parse_extra_innings(response) -> Generator:
        extra_innings_list = (
            response.xpath('//span[text()="Will there be extra innings in the game?"]')[
                0
            ]
            .xpath("../../../../../../ms-regular-group//ms-option//text()")
            .getall()
        )
        outcome_one, odds_one = clean(extra_innings_list[0]), clean(
            extra_innings_list[1]
        )
        outcome_two, odds_two = clean(extra_innings_list[2]), clean(
            extra_innings_list[3]
        )

        yield OddsItem(
            time_ns=time_ns(),
            book="BetMGM",
            sport="baseball",
            game_id=response.meta["game"],
            odds_description=f"Will there be extra innings in the game? {outcome_one}",
            odds=int(odds_one),
        )

        yield OddsItem(
            time_ns=time_ns(),
            book="BetMGM",
            sport="baseball",
            game_id=response.meta["game"],
            odds_description=f"Will there be extra innings in the game? {outcome_two}",
            odds=int(odds_two),
        )

    @baseball
    def parse_first_second_run(response) -> Generator:
        first_run_list = (
            response.xpath('//span[text()="Which team will score the 1st run?"]')[0]
            .xpath(
                '../../../../../../ms-regular-group//ms-option[@class="option ng-star-inserted"]//text()'
            )
            .getall()
        )
        second_run_list = (
            response.xpath('//span[text()="Which team will score the 2nd run?"]')[0]
            .xpath(
                '../../../../../../ms-regular-group//ms-option[@class="option ng-star-inserted"]//text()'
            )
            .getall()
        )

        frl_team_one, frl_team_odds_one = clean(first_run_list[0]), clean(
            first_run_list[1]
        )
        frl_team_two, frl_team_odds_two = clean(first_run_list[2]), clean(
            first_run_list[3]
        )

        srl_team_one, srl_team_odds_one = clean(second_run_list[0]), clean(
            second_run_list[1]
        )
        srl_team_two, srl_team_odds_two = clean(second_run_list[2]), clean(
            second_run_list[3]
        )

        yield OddsItem(
            time_ns=time_ns(),
            book="BetMGM",
            sport="baseball",
            game_id=response.meta["game"],
            odds_description=f"Which team will score the 1st run? {frl_team_one}",
            odds=int(frl_team_odds_one),
        )

        yield OddsItem(
            time_ns=time_ns(),
            book="BetMGM",
            sport="baseball",
            game_id=response.meta["game"],
            odds_description=f"Which team will score the 1st run? {frl_team_two}",
            odds=int(frl_team_odds_two),
        )

        yield OddsItem(
            time_ns=time_ns(),
            book="BetMGM",
            sport="baseball",
            game_id=response.meta["game"],
            odds_description=f"Which team will score the 2nd run? {srl_team_one}",
            odds=int(srl_team_odds_one),
        )

        yield OddsItem(
            time_ns=time_ns(),
            book="BetMGM",
            sport="baseball",
            game_id=response.meta["game"],
            odds_description=f"Which team will score the 2nd run? {srl_team_two}",
            odds=int(srl_team_odds_two),
        )

    @football
    def game_lines(response) -> Generator:
        """Parses Game Lines."""
        # TODO: Be careful here, if there's tabs, then there won't be the suffix - Full Game
        labels = (
            response.xpath("//span[text()='Game Lines - Full Game']")[0]
            .xpath("../../../../../..")[0]
            .xpath("//ms-six-pack-option-group[@class='ng-star-inserted']")[0]
            .xpath("//div[@class='six-pack-player-name']/span//text()")
            .getall()
        )
        odds = (
            response.xpath("//span[text()='Game Lines - Full Game']")[0]
            .xpath("../../../../../..")[0]
            .xpath(
                "//ms-six-pack-option-group[@class='ng-star-inserted']//ms-option[@class='option ng-star-inserted']//text()"
            )
            .getall()
        )

        team_1, team_2 = labels

        spread_team_1, spread_team_1_odds = clean(odds[0]), int(clean(odds[1]))
        spread_team_2, spread_team_2_odds = clean(odds[5]), int(clean(odds[6]))
        over_line, under_line = clean(odds[2]), clean(odds[7])
        over_odds, under_odds = int(clean(odds[3])), int(clean(odds[8]))
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
