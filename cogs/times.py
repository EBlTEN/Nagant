import json
from logging import getLogger

from discord.ext import commands

logger = getLogger(f"discord.{__name__}")

f = open("./config.json", "r")
config = json.load(f)[__name__]


class Times(commands.Cog):
    """
    カテゴリが分報_在校生､分報_仮入部生のチャンネルの自分のメッセージに📌のリアクションを飛ばすとそのメッセージをピン留めする｡\n
    他人のメッセージについた📌のリアクションは削除される｡\n
    他人のチャンネルの自分のメッセージもピン留めできてしまうので注意(修正未定)
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("File has been loaded successfully")

    # リアクションがつけられたときに呼ばれる
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # 変数
        emoji = str(payload.emoji)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(message.guild.id)
        user = guild.get_member(payload.user_id)

        # 分報カテゴリであるか
        # 自分のメッセージにつけたリアクションであるか
        if (
            channel.category.id in config["debug"]
            and message.author.id == user.id
            and emoji == "📌"
        ):
            # リアクションが赤ピンならピン留め
            await message.pin()
            logger.info("%s pinned message", user)

        # カテゴリ内の他人につけたリアクションであるか
        elif (
            channel.category.id in config["debug"]
            and message.author.id != user.id
            and emoji == "📌"
        ):
            # 赤ピンがついたら削除
            await message.remove_reaction(emoji, user)

        # カテゴリ外のリアクションには反応しない
        else:
            pass

    # リアクションが削除されたときに呼び出される｡
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # 変数
        emoji = str(payload.emoji)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(message.guild.id)
        user = guild.get_member(payload.user_id)

        # 分報カテゴリかつ赤ピンが削除された
        if (
            channel.category.id in config["debug"]
            and message.author.id == user.id
            and emoji == "📌"
        ):
            await message.unpin()
            logger.info("%s unpinned message", user)
        else:
            pass


async def setup(bot):
    await bot.add_cog(Times(bot))
