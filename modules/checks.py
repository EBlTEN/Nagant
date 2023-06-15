from typing import Union

import discord.app_commands as app_commands
from discord import Interaction
from discord.ext.commands import Context

from . import Constant, load_constant

const: Constant = load_constant()


def is_developer():
    def predicate(ctx: Union[Context, Interaction]) -> bool:
        if isinstance(ctx, Interaction):
            return ctx.user.id in const.developers
        else:
            return ctx.author.id in const.developers

    return app_commands.check(predicate)
