from discord import Game
import json
from discord.ext import commands, tasks
import dotenv
import os
from asyncio import sleep
from logging import getLogger

logger = getLogger(f"discord.{__name__}")

dotenv.load_dotenv()

STATUS = os.environ["STATUS"]
f = open("./config.json", "r")
config = json.load(f)[STATUS][__name__]


class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.display_role.start()

    def cog_unload(self):
        self.display_role.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("File has been loaded successfully")
        self.guild = self.bot.get_guild(int(config["guild"]))

    @tasks.loop()
    async def display_role(self):
        for role_id in config["role"]:
            role = self.guild.get_role(role_id)
            await self.bot.change_presence(
                activity=Game(f"{role.name} {len(role.members)}人")
            )
            await sleep(30)

    @display_role.before_loop
    async def before_display_role(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Presence(bot))
