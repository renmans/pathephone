import os
import datetime as dt
from functools import wraps
import yt_dlp
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='.', intents=intents)
vc = None

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except Exception as ex:
            write_log(str(ex))
    return wrapper


def write_log(msg, type='ERROR'):
    with open('log.txt', 'a') as f:
        f.write(f"[{type}] -- [{dt.datetime.now()}] -- {msg}\n")


@client.event
async def on_ready():
    pass


@logger
@client.event
async def on_message(message):
    global vc

    if message.author == client.user:
        return
    if message.content.startswith('$ping'):
        await message.channel.send('pong')

    if message.content.startswith('$play'):
        user = message.author
        voice_channel = user.voice.channel
        write_log(f"{user} -- {message.content}", 'INFO')

        # download audio
        link = message.content.split()[1]
        try:
            filename = f"{download_audio(link)}.mp3"
        except Exception as ex:
            write_log(ex)
            await message.channel.send(f'Can\'t find song -- {link}')

        # connect to voice channel
        if voice_channel != None and client.user not in voice_channel.members:
            write_log(f'{voice_channel} -- {voice_channel.members}', 'INFO')
            vc = await voice_channel.connect()
        else:
            write_log(f'Bot already in {voice_channel}', 'INFO')
        
        # play song
        vc.play(discord.FFmpegPCMAudio(filename))
        if not vc.is_playing():
            vc.stop()

    if message.content.startswith('$skip'):
        vc.stop()


@logger
def download_audio(link):
    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
        info_dict = video.extract_info(link, download = False)
        video_title = info_dict['title']
        if f'{video_title}.mp3' in os.listdir():
            write_log(f"\"{video_title}\" has already been downloaded", 'INFO')
            return video_title
        info_dict = video.extract_info(link, download = True)
        write_log(f"Downloading: {video_title}", 'INFO')
        video.download(link)
    return video_title


if __name__ == '__main__':
    client.run(os.environ.get('PATHEPHONE_TOKEN'))