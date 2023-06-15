from logging import getLogger

import discord
from discord import Interaction, app_commands, Embed
from discord.ext import commands
from typing import Literal
from logging import Logger

from modules import checks

logger: Logger = getLogger(f"discord.{__name__}")

layer: list[str] = []


class Presence(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        logger.info("File has been loaded successfully")

    @app_commands.command(description="Presenceを変更します。")
    @checks.is_developer()
    async def presence(
        self,
        interaction: Interaction,
        mode: Literal["clear", "list", "remove", "set"],
        presence: str | None,
    ) -> None:
        embed: Embed

        if mode == "clear":
            layer.clear()
            await self.bot.change_presence(activity=None)
            embed = discord.Embed(
                title="Success",
                description="Presence has been cleared.",
                color=0x3333CC,
            )

        elif mode == "list":
            embed = discord.Embed(
                title="Presence List", description="\n".join(layer), color=0x3333CC
            )

        elif mode == "remove":
            layer.pop(0)
            await self.bot.change_presence(activity=discord.Game(name=layer[0]))
            embed = discord.Embed(
                title="Success",
                description=f"{presence} has been removed.",
                color=0x3333CC,
            )

        elif mode == "set":
            if not presence:
                embed = discord.Embed(
                    title="Error", description="Presence is empty.", color=0xFF0000
                )
            else:
                layer.insert(0, presence)
                await self.bot.change_presence(activity=discord.Game(name=presence))
                embed = discord.Embed(
                    title="Success",
                    description=f"{presence} has been set.",
                    color=0x3333CC,
                )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot) -> None:
    await bot.add_cog(Presence(bot))
