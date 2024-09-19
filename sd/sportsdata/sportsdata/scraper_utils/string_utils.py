"""String utilities."""


def clean_string(s: str) -> str:
    """Cleans a string.

    Cases:
      Replaces em-dash with hyphen (DraftKings).

    Args:
      s: A string s to clean.

    Returns:
      A cleaned string.
    """
    s = s.replace("−", "-")
    return s.strip()
