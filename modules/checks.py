import discord.app_commands as app_commands
from discord.ext.commands import Context
from . import load_constant, Constant
from discord import Interaction

const: Constant = load_constant()


def is_developer():
    def predicate(ctx: Context | Interaction) -> bool:
        if isinstance(ctx, Interaction):
            return ctx.user.id in const.developers
        else:
            return ctx.author.id in const.developers

    return app_commands.check(predicate)
