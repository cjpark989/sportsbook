from asgiref.sync import sync_to_async
from django.db import models


# Create your models here.
class OddsItem(models.Model):
    """
    {time_ns}: Unix nanosecond timestamp representing time at which odds was taken.
    {book}: String representing the sportsbook from which the odds item was scraped.
    {sport}: String representing the sport that the odds corresponds to.
    {game_description}: Unique string representing the sports game.
    {market_description}: Standardized description for the odds market. For example, O/U 150 could be its own market.
    {plays}: A JSON-serializable list of strings that represents all possible outcomes for {market_id}. Exactly one play must win.
    {odds}: A JSON-serializable list of integers that represents the odds outcomes for {market_id}. Exactly one play must win.
    {source_url}: String representing where the OddsItem was scraped from.
    """

    time_ns = models.IntegerField(default=-1)
    book = models.CharField(max_length=200)
    sport = models.CharField(max_length=200)
    game_description = models.CharField(max_length=200, default="unknown_game")
    market_description = models.CharField(max_length=200, default="unknown_market")
    plays = models.TextField(
        null=True
    )  # json-serialize list of strings, each of which describe a play.
    odds = models.TextField(null=True)  # json-serializable list of integers
    source_url = models.CharField(max_length=1024, default="unknown_url")

    def __str__(self) -> str:
        return f"OddsItem(time_ns={self.time_ns}, book={self.book}, game_description={self.game_description}, market_description={self.market_description}, plays={self.plays}, odds={self.odds}, url={self.source_url})"
