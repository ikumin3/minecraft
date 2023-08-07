import discord
import psutil
import asyncio
import os
from dotenv import load_dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # self.target_channel_id = 548839689323544593
        await self.check_process()

    # async def on_message(self, message):
    #     print(f'Message from {message.author}: {message.content}')
        
    #     if message.content.startswith('$hello'):
    #         await message.channel.send('Hello!')
            
    async def check_process(self):
        # print(pid)
        # channel = self.get_channel(self.target_channel_id)

        while True:
            pid = get_pid('java')
            if pid is not None and is_process_running(pid):
                activity = discord.Activity(name='Minecraft is Running　　　', type=discord.ActivityType.watching)
            else:
                activity = discord.Activity(name='Minecraft is Stopped　　　', type=discord.ActivityType.watching)

            await self.change_presence(activity=activity)
            await asyncio.sleep(1800)  # Sleep for 1800 seconds

                # process = psutil.Process(pid)

            #     if is_process_running(pid):
            #         print(f"Process {pid} is runnning")
            #         # await channel.send(f"起動してます！")
            #         activity = discord.Activity(name='Minecraft is Running　　　', type=discord.ActivityType.watching)
            #         await self.change_presence(activity=activity)
            #     else:
            #         print(f"Process {pid} is not running")
            #         activity = discord.Activity(name='Minecraft is Stopped　　　', type=discord.ActivityType.watching)
            #         await self.change_presence(activity=activity)
            # except psutil.NoSuchProcess:
            #     print(f"Process {pid} does not exist.")
            #     activity = discord.Activity(name='Minecraft is Stopped', type=discord.ActivityType.watching)
            #     await self.change_presence(activity=activity)
            #     # await channel.send(f"起動してません！")
            # await asyncio.sleep(1800)  # Sleep for 5 seconds

def get_pid(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc.info['pid']
    return None

def is_process_running(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

load_dotenv()
token = os.getenv('MY_SECRET_TOKEN')
client.run(token)

