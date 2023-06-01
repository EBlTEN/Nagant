import json
import os
from logging import getLogger

import dotenv
from discord import (
    Embed,
    HTTPException,
    Message,
    MessageType,
)
from discord.ext import commands

logger = getLogger(f"discord.{__name__}")

dotenv.load_dotenv()

STATUS = os.environ["STATUS"]
f = open("./config.json", "r")
config = json.load(f)[STATUS][__name__]


class Times(commands.Cog):
    """
    特定のカテゴリの自分のメッセージに📌のリアクションを飛ばすとそのメッセージをピン留めする｡\n
    他人のメッセージについた📌のリアクションは削除される｡\n
    他人のチャンネルの自分のメッセージもピン留めできてしまうので注意(修正未定)
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        logger.info("File has been loaded successfully")

    # リアクションがつけられたときに呼ばれる
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = str(payload.emoji)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(message.guild.id)
        user = guild.get_member(payload.user_id)

        if not channel.category:
            return

        if not channel.category.id in config["times_category"]:
            return

        if not emoji == "📌":
            return

        if message.author.id == user.id:
            try:
                await message.pin()
                logger.info("%s pinned message", user)

            # ピン留めに失敗した時
            except HTTPException as err:
                embed = Embed(
                    title="Error", description="メッセージのピン留めに失敗しました｡", color=0xCC3333
                )
                embed.add_field(name=err.status, value=err.text)
                embed.set_footer(text=f"Error code:{err.code}")
                await channel.send(embed=embed)
                await message.remove_reaction(emoji, user)
                logger.error(err)

        else:
            await message.remove_reaction(emoji, user)

    # リアクションが削除されたときに呼び出される｡
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = str(payload.emoji)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(message.guild.id)
        user = guild.get_member(payload.user_id)

        if not channel.category:
            return

        if not message.pinned:
            return

        if not channel.category.id in config["times_category"]:
            return

        if not emoji == "📌":
            return

        if message.author.id == user.id:
            print(message.author.id, user.id)
            try:
                await message.unpin()
                logger.info("%s unpinned message", user)

            # ピン留めに失敗したとき
            except HTTPException as err:
                embed = Embed(
                    title="Error", description="メッセージのピン留めの解除に失敗しました｡", color=0xCC3333
                )
                embed.add_field(name=err.status, value=err.text)
                embed.set_footer(text=f"Error code:{err.code}")
                await channel.send(embed=embed)
                logger.error(err)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # カテゴリ内にピン留めメッセージが送信されたら
        if (
            message.type == MessageType.pins_add
            and message.channel.category_id in config["times_category"]
        ):
            await message.delete()


async def setup(bot):
    await bot.add_cog(Times(bot))
