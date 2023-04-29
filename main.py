import dotenv
import json
import logging
import logging.handlers
import os

import discord
from discord import Embed, Interaction, app_commands
from discord.ext import commands

# 環境変数を読み込む
dotenv.load_dotenv()

# 設定ファイルの読み込み
f = open("./config.json", "r")
config = json.load(f)[__name__]

# loggerインスタンスの生成
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.INFO)

# フォーマット
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)

# ファイルに出力するlogの設定
file_handler = logging.handlers.RotatingFileHandler(
    filename="discord.log", encoding="utf-8", maxBytes=8 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(formatter)

# コンソールに出力するlogの設定
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# loggerにhandlerを追加
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# commands.Botクラスを継承､setup_hook関数をoverride
class Nagant(commands.Bot):
    async def setup_hook(self):
        try:
            # cogsフォルダ内の.pyを読み込む
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    # extensionで読み込むことでワンタッチでリロードできる
                    await bot.load_extension(f"cogs.{filename[:-3]}")
        # エラー吐いたらログに表示
        except Exception as err:
            logger.error(err)
        # slash commandを登録
        commands = await self.tree.sync()
        logger.info("%s commands loaded", len(commands))


intents = discord.Intents.all()  # intentsの定義
bot = Nagant(command_prefix="", intents=intents, help_command=None)  # インスタンスの生成


# botの開発者かどうか判定する関数
def is_developer(interaction: Interaction) -> bool:
    owner_id = config["developer"]
    return interaction.user.id in owner_id


@bot.event
async def on_ready():
    # ログインしたらコンソールにメッセージを表示
    logger.info("Welcome to discord.py!(ver.%s)", discord.__version__)


# logファイルの送信コマンド
@bot.tree.command(description="logファイルを送信する")
@app_commands.check(is_developer)
async def log(interaction: Interaction, backup_number: int = None):
    # 引数に1~5を指定してバックアップを参照
    if backup_number != None:
        filename = f"discord.log.{backup_number}"
    # 引数なしで現在のlogを送信
    else:
        filename = "discord.log"

    # 送信処理
    log_file = discord.File(f"./{filename}", filename=filename)
    await interaction.response.send_message(file=log_file, ephemeral=True)


# cogの管理コマンド
@bot.tree.command(description="cogsフォルダ内に存在するcogの管理をする。")
@app_commands.check(is_developer)
# モードの入力補完設定
@app_commands.choices(
    mode=[
        app_commands.Choice(name="load", value="load"),
        app_commands.Choice(name="reload", value="reload"),
        app_commands.Choice(name="unload", value="unload"),
    ]
)
@app_commands.describe(cog="cogsフォルダ内のcogファイル")
async def cog(interaction: Interaction, mode: str, cog: str):
    # 各モードの処理
    if mode == "load":
        await bot.load_extension(f"cogs.{cog}")
    elif mode == "reload":
        await bot.reload_extension(f"cogs.{cog}")
    elif mode == "unload":
        await bot.unload_extension(f"cogs.{cog}")

    embed = Embed(
        title="Success",
        description=f"{cog} has been {mode}ed.",
        color=0x3333CC,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    logger.info("%s has been %sed.", cog, mode)


# 各コマンドのエラーハンドリング
@log.error
async def log_error(interaction: Interaction, err):
    embed = Embed(title="Error", description=err, color=0xCC3333)
    await interaction.response.send_message(embed=embed, ephemeral=True)


if __name__ == "__main__":
    TOKEN = os.environ["DISCORD_TOKEN"]
    # Bot本体の起動
    bot.run(TOKEN, log_handler=None)
