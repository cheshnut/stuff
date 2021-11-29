from block_io import BlockIo
from discord.ext import commands
from discord.utils import get
import discord
import json

#Block-io API
version = 2 # API version
block_io = BlockIo('API KEY', 'SECRET KEY', version)

intents = discord.Intents().all()

bot = commands.Bot(command_prefix ="a!", case_insensitive=True, intents = intents)

@bot.event
async def on_ready():
  print("Bot is ready.")

@bot.command()
async def stash(ctx):
  #Writing Output to json file so it looks good
  json_object = json.dumps(block_io.get_balance(), indent = 4)
  with open("WalletOutputApi.json", "w") as outfile:
    outfile.write(json_object)
  
  wallets = await get_wallet_data()
  user = bot.get_user(ctx.author.id)
  emoji = discord.utils.get(bot.emojis, name='BtcEmoji')

  if wallets["status"] == "fail":
    await ctx.send("Block-io API fail please try again")
    return False
  else:
    status = wallets["status"]
    wallet_amt = wallets["data"]["available_balance"] 
    network = wallets["data"]["network"]
    pending = wallets["data"]["pending_received_balance"]

    embed = discord.Embed(title=f"Bitcoin Address : **`bc1qfcw3er0e20uupya72ye3rg97efg8eqcaqs53t8um83nkp6epmwhs80mmy2`** {emoji} ", value=emoji)
    embed.set_author(name=ctx.author.name, icon_url=user.avatar_url)
    embed.add_field(name="Status", value=f"`{status}`")
    embed.add_field(name="Format", value="`BECH32 (P2WSH)`", inline=False)
    embed.add_field(name="Wallet Balance", value=f"`{wallet_amt} BTC` {emoji}", inline=False)
    embed.add_field(name="Wallet Network", value=f"`{network}` {emoji}", inline=False)
    embed.add_field(name="Pending Transaction", value=f"`{pending} BTC` {emoji}", inline=False)
    embed.add_field(name=f"Fresh Output no edits", value=f"`{block_io.get_balance()}`", inline=False)

    await ctx.send(embed=embed)
  
#Reading Json File
async def get_wallet_data():
  with open("WalletOutputApi.json", "r") as f:
    wallet = json.load(f) 
      
    return wallet

bot.run("TOKEN")
