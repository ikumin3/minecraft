import discord
import psutil
import asyncio
import os
from dotenv import load_dotenv
import subprocess
import time
import re

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # self.target_channel_id = 548839689323544593
        await self.check_process()

    # async def on_message(self, message):
    #     print(f'Message from {message.author}: {message.content}')
        
    #     if message.content.startswith('$hello'):
    #         await message.channel.send('Hello!')
    
    # 非同期javaプロセス監視関数
    async def check_process(self):
        # print(pid)
        # channel = self.get_channel(self.target_channel_id)

        while True:
            pid = get_pid('java')
            player_count = get_member_num()
            if pid is not None and is_process_running(pid):
                activity = discord.Activity(name=f'{player_count} 人が Minecraft ', type=discord.ActivityType.playing)
            else:
                activity = discord.Activity(name='Minecraft is Stopped　　　', type=discord.ActivityType.watching)

            await self.change_presence(activity=activity)
            await asyncio.sleep(300)  # Sleep for 1800 seconds

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
    
def get_member_num():
    try:
        subprocess.run(["screen","-S","minecraft","-X","stuff","list\n"])
        time.sleep(5)
    except:
        print(f"Error subprocess")
        return 0
        
    try:
        with open("/home/ubuntu/opt/minecraft/logs/latest.log") as file:
            lines = file.readlines()
    except:
        print(f"Error file open")
        return 0
    
    for line in reversed(lines):
        print(line)
        match = None
        if "There are" in line:
            try:
                match = re.search("There are (\d+) of a max of 20 players online:",line)
            except:
                print(f"Error match")
                continue
        if match:
            player_count = int(match.group(1))
            return player_count
    return 0

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

load_dotenv()
token = os.getenv('MY_SECRET_TOKEN')
client.run(token)

