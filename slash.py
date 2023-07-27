import discord

bot = discord.Bot()
token = "bot_token"


@bot.event
async def on_ready():
  print("봇이 작동합니다.")


@bot.slash_command(description="Check bot's response latency")
async def ping(ctx):
  embed = discord.Embed(title="Pong!", description=f"Delay: {bot.latency} seconds", color=0xFFFFFF)
  embed.set_footer(text="Embed Footer")
  await ctx.respond(embed=embed)


bot.run(token)
