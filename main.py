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

@bot.command()
async def gs(ctx, keyword: str):
    await ctx.send("**Searching...**")
    search_results = []

    # SerpApi - Google search로 리퀘스트 보냄
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
        await ctx.send(f"**요청하신 키워드 '{keyword}'에 대한 검색 결과입니다:**")
        await ctx.send("\n".join(search_results))
    else:
        await ctx.send(f"**요청하신 키워드 '{keyword}'에 대한 검색 결과를 찾을 수 없습니다.**")

@bot.command()
async def gis(ctx, keyword: str):
    await ctx.send("**Searching...**")
    # SerpApi - Google Image Search로 리퀘스트 보냄
    params = {
        "api_key": SERPAPI_KEY,
        "q": keyword,
        "tbm": "isch"  # 이미지 검색을 위한 매개변수
    }
    response = requests.get("https://serpapi.com/search", params=params)

    # JSON response 파싱하기
    results = response.json().get("images_results")

    # Send the first image to the Discord chat
    if results:
        image_url = results[0].get("original")
        await ctx.send(f"**요청하신 키워드 '{keyword}'에 대한 이미지 검색 결과입니다:**")
        await ctx.send(image_url)

bot.run(BOT_TOKEN)
