# Source Code Made By 4rNe5(@4rNe5)
# This Code is MIT Licence
# Special Thanks For babihoba(@8954sood) & Jombi(@jombidev)

import requests
import json
import discord
from discord.ext import commands

with open("./config.json", "r", encoding="utf-8") as E:
    config = json.loads(E.read())

BOT_TOKEN = config['BOT_TOKEN']
SERPAPI_KEY = config['SERPAPI_KEY']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)


@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name="Google 검색"))


@bot.command()
async def gs(ctx, *args): # Google Search Command
    keyword = " ".join(args)
    mes = await ctx.send(f"**Searching '{keyword}' On Google...**")
    search_results = []

    # SerpApi - Google search로 검색 리퀘스트 보냄
    params = {
        "api_key": SERPAPI_KEY,
        "q": keyword,
    }
    response = requests.get("https://serpapi.com/search", params=params)

    # JSON response 파싱하기
    results = response.json().get("organic_results")

    # Accumulate the search results
    for result in results:
        title = result.get("title")
        url = result.get("link")
        if title and url:
            search_results.append(f"{title} - {url}")

    # Send all search results to the Discord chat
    if search_results:
        await ctx.message.delete()
        await ctx.send(f"**요청하신 키워드인 '{keyword}'에 대한 검색 결과입니다 :**")
        await ctx.send("\n".join(search_results))
    else:
        await ctx.message.delete()
        await ctx.send(f"**요청하신 키워드인 '{keyword}'에 대한 검색 결과를 찾을 수 없습니다.**")


@bot.command()
async def gis(ctx, *args):  # Google Image Search Command
  count = 1  # Default image count
  keyword_args = args

  # If the first argument is a number, use it as the count and remove it from the keyword arguments
  if args and args[0].isdigit():
    count = int(args[0])
    keyword_args = args[1:]

  keyword = " ".join(keyword_args)

  await ctx.send(f"**Searching '{keyword}' Image On Google...**")

  params = {
    "api_key": SERPAPI_KEY,
    "q": keyword,
    "tbm": "isch"
  }

  response = requests.get("https://serpapi.com/search", params=params)

  results = response.json().get("images_results")

  if results:
    await ctx.message.delete()
    await ctx.send(f"**요청하신 키워드인 '{keyword}'에 대한 이미지 검색 결과(__{count}장__)입니다 :**")

    for result in results[:count]:
      image_url = result.get("original")
      if image_url:
        await ctx.send(image_url)


bot.run(BOT_TOKEN) # 봇 실행
