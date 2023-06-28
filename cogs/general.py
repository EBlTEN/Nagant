from discord import app_commands, Interaction
from discord.ext import commands
from logging import getLogger

logger = getLogger(f"discord.{__name__}")


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self) -> None:
        logger.info("File has been loaded successfully")

    @app_commands.command(description="GitHubのリポジトリを表示します。")
    async def github(self, interaction: Interaction) -> None:
        await interaction.response.send_message(
            "https://github.com/EBlTEN/Nagant", ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(General(bot))
