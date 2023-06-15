from dataclasses import dataclass
from os import environ
from sys import argv

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Constant:
    DISCORD_TOKEN: str = environ["DISCORD_TOKEN"]
    developers: tuple[int, ...] = (501340685757186059,)
    times_category: tuple[int, ...] = (1091405095326990508, 1091405342543462502)


@dataclass(frozen=True)
class DevelopmentConstant(Constant):
    times_category: tuple[int] = (1056237732957012038,)


def load_constant() -> Constant:
    try:
        if argv[1] == "debug":
            return DevelopmentConstant()
        else:
            return Constant()
    except IndexError:
        return Constant()
