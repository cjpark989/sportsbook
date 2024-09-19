# Scrapers

## Introduction

This directory contains several web scrapers for sportsdata. There is one Scrapy webscraper for each sportsbook, and the webscrapers use their corresponding parser files under `sd/sportsdata/sportsdata/scraper_utils/parsers` to parse odds items for that website. There is a different parser for each sport, and it is specified via a meta field.  

Scrapers must yield `OddsItem` objects, which are Django models. Upon being yielded, the Django models are automatically stored in an sqlite database. The scraped odds are subsequently displayed in the UI. 

## OddsItem Schema

1. `{time_ns}`: Unix nanosecond timestamp representing time at which odds was taken.
2. `{book}`: String representing the sportsbook from which the odds item was scraped.
3. `{sport}`: String representing the sport that the odds corresponds to.
4. `{game_description}`: Unique string representing the sports game.
5. `{market_description}`: Standardized description for the odds market. For example, O/U 150 could be its own market.
6. `{plays}`: A JSON-serializable list of strings that represents all possible outcomes for {market_id}. Exactly one play must win.
7. `{odds}`: A JSON-serializable list of integers that represents the odds outcomes for {market_id}. Exactly one play must win.
8. `{source_url}`: String representing where the OddsItem was scraped from.

## Market Descriptions

Market descriptions are standardized across sportsbooks so that one can easily compare odds for the same market across the sportsbook. Below is a table depicting the standard descriptions that we use:



| market_description | Use case    | 
| :----:             | :----:      | 
| `Moneyline`        | This market description is used to describe whether one team will outright win or lose the sporting event.       | 
