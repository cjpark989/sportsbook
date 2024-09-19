import time


def decimal_odds_to_american_odds(odds: float) -> float:
  if odds >= 2:
    return 100 * (odds - 1)
  return 100 / (1 - odds)