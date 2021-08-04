"""Cryptocurrency Controller"""
__docformat__ = "numpy"
# pylint: disable=R0904, C0302, R1710
import argparse
import os
import matplotlib.pyplot as plt
import pandas as pd
from prompt_toolkit.completion import NestedCompleter
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import get_flair
from gamestonk_terminal.menu import session
from gamestonk_terminal.cryptocurrency.overview import overview_controller
from gamestonk_terminal.cryptocurrency.due_dilligence import dd_controller
from gamestonk_terminal.cryptocurrency.discovery import discovery_controller
from gamestonk_terminal.cryptocurrency.due_dilligence import (
    pycoingecko_view,
    coinpaprika_view,
    binance_model,
)

from gamestonk_terminal.cryptocurrency import load


class CryptoController:

    CHOICES = [
        "?",
        "cls",
        "help",
        "q",
        "quit",
        "ta",
        "load",
        "clear",
        "chart",
        "dd",
        "ov",
        "disc",
    ]

    def __init__(self):
        """CONSTRUCTOR"""

        self.crypto_parser = argparse.ArgumentParser(add_help=False, prog="crypto")
        self.crypto_parser.add_argument("cmd", choices=self.CHOICES)

        self.current_coin = None
        self.current_df = pd.DataFrame()
        self.current_currency = None
        self.source = ""

    def print_help(self):
        """Print help"""
        print(
            "https://github.com/GamestonkTerminal/GamestonkTerminal/tree/main/gamestonk_terminal/cryptocurrency"
        )
        print("\nCryptocurrency:")
        print("   cls             clear screen")
        print("   ?/help          show this menu again")
        print("   q               quit this menu, and shows back to main menu")
        print("   quit            quit to abandon program")
        print("   finbrain        Crypto sentiment from 15+ major news headlines")
        print("")
        print(f"Loaded coin: {self.current_coin}")
        print("")
        print(">  ov              Coinmarketcap menu")
        print(">  disc            Binance menu with order book, candles, ta.. ")

        if self.current_coin:
            print(">  dd              CoinPaprika menu")
            print(">  ta")
            print(">  chart")

        print("")

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

        (known_args, other_args) = self.crypto_parser.parse_known_args(an_input.split())

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
        """Process Q command - quit the menu"""
        return False

    def call_quit(self, _):
        """Process Quit command - quit the program"""
        return True

    def call_load(self, other_args):
        """Process load command"""
        try:
            (
                self.current_coin,
                self.current_currency,
                self.current_df,
                self.source,
            ) = load(other_args)
            print(f"Loaded coin {self.current_coin}\n")
        except TypeError:
            print("Couldn't load data\n")

    def call_chart(self, other_args):
        """Process view command"""
        if self.current_coin:
            if self.source == "cg":
                pycoingecko_view.chart(self.current_coin, other_args)
            elif self.source == "bin":
                binance_model.show_candles(
                    self.current_df, self.current_coin, self.current_currency
                )
            elif self.source == "cp":
                coinpaprika_view.chart(self.current_coin, other_args)
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_clear(self, _):
        """Process clear command"""
        if self.current_coin:
            print(
                f"Current coin {self.current_coin} was removed. You can load new coin with load -c <coin>"
            )
            print("")
            self.current_coin = None
            self.current_currency = None
            self.current_df = pd.DataFrame()
        else:
            print("No coin selected. Use 'load' to load the coin you want to look at.")
            print("")

    def call_disc(self, _):
        """Process disc command"""
        return discovery_controller.menu()

    def call_ov(self, _):
        """Process disc command"""
        return overview_controller.menu()

    def call_dd(self, _):
        """Process dd command"""
        if self.current_coin:
            return dd_controller.menu(self.current_coin, self.source)

        print("No coin selected. Use 'load' to load the coin you want to look at.")
        print("")


def menu():
    crypto_controller = CryptoController()
    crypto_controller.print_help()
    plt.close("all")
    while True:
        # Get input command from user
        if session and gtff.USE_PROMPT_TOOLKIT:
            completer = NestedCompleter.from_nested_dict(
                {c: None for c in crypto_controller.CHOICES}
            )
            an_input = session.prompt(
                f"{get_flair()} (crypto)> ",
                completer=completer,
            )
        else:
            an_input = input(f"{get_flair()} (crypto)> ")

        try:
            process_input = crypto_controller.switch(an_input)

            if process_input is not None:
                return process_input

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue
