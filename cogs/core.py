from logging import getLogger
from typing import Literal, Optional

import discord
from discord import Embed, app_commands, Interaction
from discord.ext import commands
from discord.ext.commands import Context

from modules import checks

logger = getLogger(f"discord.{__name__}")


class Core(commands.Cog):
    """
    botの管理用コマンド
    デバッグ用のサーバーでのみ実行可能
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self) -> None:
        logger.info("File has been loaded successfully")

    # send log file
    @commands.hybrid_command()
    @checks.is_developer()
    async def log(self, ctx: Context, backup_number: Optional[int]) -> None:
        filename: str
        if backup_number != None:
            filename = f"discord.log.{backup_number}"
        else:
            filename = "discord.log"

        log_file = discord.File(f"./{filename}", filename=filename)
        await ctx.send(file=log_file)

    # manage cogs
    @commands.hybrid_command()
    @checks.is_developer()
    @app_commands.describe(cog="cogsフォルダ内のcogファイル")
    async def cog(
        self,
        ctx: Context,
        mode: Literal[
            "load",
            "reload",
            "unload",
        ],
        cog: str,
    ) -> None:
        if mode == "load":
            await self.bot.load_extension(f"cogs.{cog}")
        elif mode == "reload":
            await self.bot.reload_extension(f"cogs.{cog}")
        elif mode == "unload":
            await self.bot.unload_extension(f"cogs.{cog}")

        embed: Embed = Embed(
            title="Success",
            description=f"{cog} has been {mode}ed.",
            color=0x3333CC,
        )
        await ctx.send(embed=embed)
        logger.info("%s has been %sed.", cog, mode)


async def setup(bot) -> None:
    await bot.add_cog(Core(bot), guild=discord.Object(681015774885838896))
