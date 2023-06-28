from dataclasses import dataclass
from logging import getLogger
from typing import Any, Optional, Union

from discord import (
    Embed,
    HTTPException,
    Member,
    Message,
    MessageType,
    TextChannel,
    Thread,
)
from discord.ext import commands

from modules import Constant, FetchDataError, load_constant

logger = getLogger(f"discord.{__name__}")

const: Constant = load_constant()


@dataclass
class ReceiveData:
    emoji: str
    channel: Union[TextChannel, Thread]
    message: Message
    category_id: Optional[int]
    member: Member


class Times(commands.Cog):
    """
    特定のカテゴリの自分のメッセージに📌のリアクションを飛ばすとそのメッセージをピン留めする｡\n
    他人のメッセージについた📌のリアクションは削除される｡\n
    他人のチャンネルの自分のメッセージもピン留めできてしまうので注意(修正未定)
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        logger.info("File has been loaded successfully")

    async def get_args(self, payload: Any) -> ReceiveData:
        emoji: str = str(payload.emoji)
        channel: Union[TextChannel, Thread] = self.bot.get_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        category_id: Optional[int] = channel.category_id

        if not message.guild:
            raise FetchDataError("Failed to get guild.")
        member: Optional[Member] = message.guild.get_member(payload.user_id)

        if not member:
            raise FetchDataError("Failed to get member.")

        return ReceiveData(emoji, channel, message, category_id, member)

    # add reaction to message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload) -> None:
        args: ReceiveData = await self.get_args(payload)

        if not args.category_id in const.times_category:
            return

        if not args.emoji == "📌":
            return

        if args.message.author.id == args.member.id:
            try:
                await args.message.pin()
                logger.info("%s pinned message", args.member)

            # failed to pin message
            except HTTPException as err:
                embed: Embed = Embed(
                    title="Error", description="メッセージのピン留めに失敗しました｡", color=0xCC3333
                )
                embed.add_field(name=err.status, value=err.text)
                embed.set_footer(text=f"Error code:{err.code}")
                await args.channel.send(embed=embed)
                await args.message.remove_reaction(args.emoji, args.member)
                logger.error(err)

        else:
            await args.message.remove_reaction(args.emoji, args.member)

    # remove reaction from message
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: Any) -> None:
        args: ReceiveData = await self.get_args(payload)
        if not args.message.pinned:
            return

        if not args.category_id in const.times_category:
            return

        if not args.emoji == "📌":
            return

        if args.message.author.id == args.member.id:
            try:
                await args.message.unpin()
                logger.info("%s unpinned message", args.member)

            # failed to unpin message
            except HTTPException as err:
                embed: Embed = Embed(
                    title="Error", description="メッセージのピン留めの解除に失敗しました｡", color=0xCC3333
                )
                embed.add_field(name=err.status, value=err.text)
                embed.set_footer(text=f"Error code:{err.code}")
                await args.channel.send(embed=embed)
                logger.error(err)

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not type(message.channel) is TextChannel or type(Thread) is Thread:
            return

        if not message.type == MessageType.pins_add:
            return

        if message.channel.category_id in const.times_category:
            await message.delete()


async def setup(bot):
    await bot.add_cog(Times(bot))
