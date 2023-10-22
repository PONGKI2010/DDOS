import discord
from discord.ext import commands
import aiohttp
import asyncio

bot = commands.Bot(command_prefix='/')
session = None  # aiohttp 세션
request_count = 0  # 요청 카운트 초기화

@bot.event
async def on_ready():
    global session
    session = aiohttp.ClientSession()
    print(f'봇 {bot.user.name}이(가) 준비되었습니다.')

@bot.command()
async def 부하테스트(ctx, 웹사이트링크: str):
    global request_count
    request_count = 0  # 요청 카운트 초기화
    await ctx.send(f"웹사이트 {웹사이트링크}에 대량 요청을 시작합니다.")
    
    tasks = [do_request(웹사이트링크, ctx) for _ in range(10)]
    await asyncio.gather(*tasks)

async def do_request(웹사이트링크, ctx):
    global request_count
    while True:
        async with session.get(웹사이트링크) as response:
            request_count += 1
            await ctx.send(f"현재까지 {request_count}번의 요청을 보냈습니다.")
            await asyncio.sleep(1)

@bot.command()
async def 중지(ctx):
    await ctx.send("웹사이트 요청을 중지합니다.")
    await session.close()
    await bot.logout()

bot.run('MTE2NTI0MzcwMzUwNjUyMjIzMg.G_1MEQ.qoRIb2msXzLiH8kUO4-WAZLpPzJG_lKQeIib_A')
