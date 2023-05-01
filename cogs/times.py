import json
import os
from logging import getLogger

import dotenv
from discord import Embed, HTTPException, Message, MessageType
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

    async def extract_args():
        pass

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
        try:
            # 分報カテゴリであるか
            # 自分のメッセージにつけたリアクションであるか
            if (
                channel.category.id in config["times_category"]
                and message.author.id == user.id
                and emoji == "📌"
            ):
                # リアクションが赤ピンならピン留め
                await message.pin()
                logger.info("%s pinned message", user)

            # カテゴリ内の他人につけたリアクションであるか
            elif (
                channel.category.id in config["times_category"]
                and message.author.id != user.id
                and emoji == "📌"
            ):
                # 赤ピンがついたら削除
                await message.remove_reaction(emoji, user)

            # カテゴリ外のリアクションには反応しない
            else:
                pass
        # カテゴリに属さないチャンネルのカテゴリidを参照したとき
        except AttributeError:
            pass
        # ピン留めに失敗したとき
        except HTTPException as err:
            # 埋め込みメッセージの作成
            embed = Embed(
                title="Error", description="メッセージのピン留めに失敗しました｡", color=0xCC3333
            )
            embed.add_field(name=err.status, value=err.text)
            embed.set_footer(text=f"Error code:{err.code}")
            await channel.send(embed=embed)
            await message.remove_reaction(emoji, user)
            logger.error(err)

    # リアクションが削除されたときに呼び出される｡
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # 変数
        emoji = str(payload.emoji)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(message.guild.id)
        user = guild.get_member(payload.user_id)

        try:
            # 分報カテゴリかつ赤ピンが削除された
            if (
                channel.category.id in config["times_category"]
                and message.author.id == user.id
                and emoji == "📌"
            ):
                await message.unpin()
                logger.info("%s unpinned message", user)
            else:
                pass
        except AttributeError:
            pass
        # ピン留めに失敗したとき
        except HTTPException as err:
            # 埋め込みメッセージの作成
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
            # 削除
            await message.delete()


async def setup(bot):
    await bot.add_cog(Times(bot))
