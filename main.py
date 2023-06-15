from os.path import basename
from pathlib import Path

from discord import Intents
from discord.app_commands import AppCommand
from discord.ext import commands
from logging import Logger

import modules

logger: Logger = modules.set_logger()


class Nagant(commands.Bot):
    async def setup_hook(self) -> None:
        # load cogs
        for cog in {f"cogs.{basename(f)[:-3]}" for f in Path("./cogs").glob("*.py")}:
            await bot.load_extension(cog)

        commands: list[AppCommand] = await self.tree.sync()
        logger.info("Loaded %s commands", len(commands))


# create bot instance
bot = Nagant(command_prefix="ng/", intents=Intents.all(), help_command=None)


@bot.event
async def on_ready() -> None:
    logger.info("Logged in as %s", bot.user)


if __name__ == "__main__":
    const = modules.load_constant()
    bot.run(const.DISCORD_TOKEN, log_handler=None)
