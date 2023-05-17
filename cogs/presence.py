import json
from logging import getLogger
import datetime

import discord
import requests
from discord.ext import commands, tasks

logger = getLogger(f"discord.{__name__}")

try:
    f = open("./config.json", "r")
    config = json.load(f)[__name__]
except KeyError:
    pass

url = "https://weather.tsukumijima.net/api/forecast/city/140010"

JST = datetime.timezone(datetime.timedelta(hours=9))


class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.display_tomorrow_wether.start()

    def get_wether():
        if datetime.datetime.now().hour >= 20:
            day = 1
        else:
            day = 0
        try:
            response = requests.get(url)
            wether = json.loads(response.text)
            date = wether["forecasts"][day]["dateLabel"]
            telop = wether["forecasts"][day]["telop"]
            max_temp = wether["forecasts"][day]["temperature"]["max"]["celsius"]

            return f"{date} {telop} 最高気温:{max_temp}℃"

        except:
            return "データの取得に失敗しました｡"

    async def cog_load(self):
        logger.info("File has been loaded successfully")

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Game(name=Presence.get_wether())
        await self.bot.change_presence(activity=activity)

    @tasks.loop(minutes=15)
    async def display_tomorrow_wether(self):
        Presence.get_wether()


async def setup(bot):
    await bot.add_cog(Presence(bot))
