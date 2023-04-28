import os
import datetime as dt
import yt_dlp
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


def download_audio(link):
    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
        info_dict = video.extract_info(link, download = False)
        video_title = info_dict['title']
        if f'{video_title}.mp3' in os.listdir():
            print(f"[INFO] -- \"{video_title}\" has already been downloaded")
            return video_title
        info_dict = video.extract_info(link, download = True)
        print(f"[INFO] -- Downloading: {video_title}")
        video.download(link)
    return video_title

if __name__ == '__main__':
    client.run(os.environ.get('PATHEPHONE_TOKEN'))