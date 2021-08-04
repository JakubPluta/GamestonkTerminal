"""Cryptocurrency Overview Controller"""
__docformat__ = "numpy"
# pylint: disable=R0904, C0302, W0622
import argparse
import os
from typing import Any
import pandas as pd
from prompt_toolkit.completion import NestedCompleter
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import get_flair
from gamestonk_terminal.menu import session
from gamestonk_terminal.cryptocurrency.due_dilligence import (
    pycoingecko_view,
    coinpaprika_view,
    finbrain_crypto_view,
    binance_model,
)


class Controller:

    CHOICES = [
        "?",
        "cls",
        "help",
        "q",
        "quit",
        "finbrain",
    ]

    PAPRIKA_CHOICES = [
        "events",
        "twitter",
        "ex",
        "mkt",
        "ta",
        "ps",
        "basic",
    ]

    GECKO_CHOICES = [
        "info",
        "market",
        "ath",
        "atl",
        "score",
        "web",
        "social",
        "bc",
        "dev",
    ]

    BINANCE_CHOICES = [
        "book",
        "candle",
        "balance",
    ]

    def __init__(self, coin: Any = None, source: str = None):
        """CONSTRUCTOR"""

        self._dd_parser = argparse.ArgumentParser(add_help=False, prog="dd")

        self.current_coin = coin
        self.current_currency = None
        self.current_df = pd.DataFrame()
        self.source = source

        if self.source == "cg":
            self.CHOICES.extend(self.GECKO_CHOICES)

        if self.source == "cp":
            self.CHOICES.extend(self.PAPRIKA_CHOICES)

        if self.source == "bin":
            self.CHOICES.extend(self.BINANCE_CHOICES)

        self._dd_parser.add_argument("cmd", choices=self.CHOICES)

    def print_paprika(self):
        print("CoinPaprika:")
        print("   basic           basic information about loaded coin")
        print("   ps              price and supply related metrics for loaded coin")
        print("   mkt             all markets for loaded coin")
        print("   ex              all exchanges where loaded coin is listed")
        print("   twitter         tweets for loaded coin")
        print("   events          events related to loaded coin")
        print("")

    def print_gecko(self):
        print("CoinGecko:")
        print("   info            basic information about loaded coin")
        print("   market          market stats about loaded coin")
        print("   ath             all time high related stats for loaded coin")
        print("   atl             all time low related stats for loaded coin")
        print("   web             found websites for loaded coin e.g forum, homepage")
        print(
            "   social          social portals urls for loaded coin, e.g reddit, twitter"
        )
        print(
            "   score           different kind of scores for loaded coin, e.g developer score, sentiment score"
        )
        print("   dev             github, bitbucket coin development statistics")
        print("   bc              links to blockchain explorers for loaded coin")
        print("")

    def print_binance(self):
        print("Binance:")
        print("   book          show order book")
        print("   candle        show candles")
        print("   balance       show coin balance")
        print("")

    def print_help(self):
        """Print help"""
        print("\nDiscovery:")
        print("   cls             clear screen")
        print("   ?/help          show this menu again")
        print("   q               quit this menu, and shows back to main menu")
        print("   quit            quit to abandon program")
        print("")
        if self.source == "cg":
            self.print_gecko()
        if self.source == "cp":
            self.print_paprika()
        if self.source == "bin":
            self.print_binance()

    def switch(self, an_input: str):
        """Process and dispatch input

        Returns
        -------
        True, False or None
            False - quit the menu
            True - quit the program
            None - continue in the menu
        """

        # Empty command
        if not an_input:
            print("")
            return None

        (known_args, other_args) = self._dd_parser.parse_known_args(an_input.split())

        # Help menu again
        if known_args.cmd == "?":
            self.print_help()
            return None

        # Clear screen
        if known_args.cmd == "cls":
            os.system("cls||clear")
            return None

        return getattr(
            self, "call_" + known_args.cmd, lambda: "Command not recognized!"
        )(other_args)

    def call_help(self, _):
        """Process Help command"""
        self.print_help()

    def call_q(self, _):
        """Process Q command - quit the menu."""
        print("Moving back to (crypto) menu")
        return False

    def call_quit(self, _):
        """Process Quit command - quit the program."""
        return True

    def call_info(self, other_args):
        """Process info command"""
        if self.current_coin:
            pycoingecko_view.info(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_market(self, other_args):
        """Process market command"""
        if self.current_coin:
            pycoingecko_view.market(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_web(self, other_args):
        """Process web command"""
        if self.current_coin:
            pycoingecko_view.web(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_social(self, other_args):
        """Process social command"""
        if self.current_coin:
            pycoingecko_view.social(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_dev(self, other_args):
        """Process dev command"""
        if self.current_coin:
            pycoingecko_view.dev(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_ath(self, other_args):
        """Process ath command"""
        if self.current_coin:
            pycoingecko_view.ath(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_atl(self, other_args):
        """Process atl command"""
        if self.current_coin:
            pycoingecko_view.atl(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_score(self, other_args):
        """Process score command"""
        if self.current_coin:
            pycoingecko_view.score(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_bc(self, other_args):
        """Process bc command"""
        if self.current_coin:
            pycoingecko_view.bc(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    # binance
    def call_book(self, other_args):
        """Process book command"""
        binance_model.order_book(other_args, self.current_coin, self.current_currency)

    def call_balance(self, _):
        """Process balance command"""
        binance_model.balance(self.current_coin)

    # paprika
    def call_ps(self, other_args):
        """Process ps command"""
        if self.current_coin:
            coinpaprika_view.price_supply(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_basic(self, other_args):
        """Process ps command"""
        if self.current_coin:
            coinpaprika_view.basic(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_mkt(self, other_args):
        """Process market command"""
        if self.current_coin:
            coinpaprika_view.markets(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_ex(self, other_args):
        """Process ex command"""
        if self.current_coin:
            coinpaprika_view.exchanges(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_events(self, other_args):
        """Process events command"""
        if self.current_coin:
            coinpaprika_view.events(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_twitter(self, other_args):
        """Process twitter command"""
        if self.current_coin:
            coinpaprika_view.twitter(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    # paprika
    def call_finbrain(self, other_args):
        """Process sentiment command"""
        finbrain_crypto_view.crypto_sentiment_analysis(other_args=other_args)


def menu(coin=None, source=None):

    source = source if source else "cg"
    controller = Controller(coin=coin, source=source)
    controller.print_help()

    while True:
        # Get input command from user
        if session and gtff.USE_PROMPT_TOOLKIT:
            completer = NestedCompleter.from_nested_dict(
                {c: None for c in controller.CHOICES}
            )
            an_input = session.prompt(
                f"{get_flair()} (crypto)>(disc)> ",
                completer=completer,
            )
        else:
            an_input = input(f"{get_flair()} (crypto)>(disc)> ")

        try:
            process_input = controller.switch(an_input)

            if process_input is not None:
                return process_input

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue
