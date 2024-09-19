# Sports Data

The purpose of the `sd` repository is to maintain web scrapers for several popular sports betting websties. It also contains a UI that can be used to quickly monitor odds across different sports websites.  

## Table of Contents
1. [Terminology](#terminology)

2. [Installation](#installation)

    1.1) [Prerequisites](#11-prerequisites)

    1.2) [Installing](#12-installing)

## 1) Terminology

The `sd` repository repeteadly uses several terms, each of which are defined below:

1. *Sportsbook:* An independent venue that accepts bets on sports such as Fanduel or Draftkings.
2. *Game*: A particular sporting event that takes place, often between two or more teams.
3. *Market*: A particular outcome on a game. Sportsbooks typically offer several different markets for a fixed game.  
4. *Binary market:* A market in which there are only two possibly outcomes. If Team A is playing Team B, Team A moneyline would be a binary market (assuming there are no ties). Total points over/under 150.5 would also be a binary outcome.
5. *n-ary market*: A market in which there are exactly $n$ possible outcomes. If Team A plays Team B and there is a possibility of a tie, this would be a $3$-ary (or *ternary market*) because there are exactly three possible outcomes.
6. *Vig/Vigorish/Juice*: The vig on a market corresponds to the "hold" that a sportsbook takes on a particular market. It is the percentage that represents the amount of money that you would lose by betting all possible outcomes in a market. Several U.S. sportsbooks quote -110 odds for seemingly 50/50 bets, which would correspond to a vig of 4.7%. 

## 2) Installation <a name="#installation">
### 2.1) Prerequisites
To run this, you must install chromedriver: https://chromedriver.chromium.org/downloads.

* If you are running Windows, move `chromedriver.exe` to `C:/Selenium/chromedriver.exe`
* If you are running Linux or MacOS, set the **chromedriver** environment variable to the path of the executable. For example, you can move it to `/usr/local/bin/`.

### 2.2) Installing
```
python -m venv venv
. venv/Scripts/activate or . venv/bin/activate
make install
```

### 2.3) Running Scrapers Locally
```
cd sportsdata
scrapy crawl [Book Name]
```

### 2.3) Running UI Locally
```
cd ui/
./deploy.sh
```

## Make Utilities

### Formatting
```
make format
```

### Installing Requirements
```
make install
```

### Supported Scrapers and Sports
* DraftKings
    * Football
    * Baseball
* BetMGM
* PointsBet
* Unibet
* FanDuel\*
* Bet365\*
* Betway
* betJACK
* Tipico (Difficult DOM)

\* = has anti-bot detection.
### Planned Support
* Hard Rock Sportsbook (App Only?)
* Barstool Sports (App Only?)
* WynnBet (App Only?)
* Caesar Entertainment (App Only?) - https://sportsbook.caesars.com/us/nj/bet/
* Betfred
* BetRivers Sportsbook
