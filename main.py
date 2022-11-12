import discord
import configparser
from discord.ext import commands

PREFIX='>'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
  await checkVoice()
  print("Bot is alive")

async def checkVoice():
    info = open('serverInfo.txt')
    lines = info.read().splitlines()
    info.close()
    if(len(lines) == 0):
        print("serverInfo.txt is null");
        return
    guild = bot.get_guild(int(lines[0]))
    category = discord.utils.get(guild.categories, id=int(lines[2]))
    channels = category.channels
    for channel in channels:
        if(str(len(channel.members)) != "0" or channel.id == int(lines[1])): continue
        if type(channel) != discord.channel.VoiceChannel or channel is None:
            print("No channel found!")
        else:
            await channel.delete()

def main():
  return "Your bot is alive!"

@bot.command()
async def reg(ctx, channelId):
    if not ctx.message.author.guild_permissions.administrator:
        return
    info = ""
    channel = discord.utils.get(ctx.guild.channels, id = int(channelId))
    cat = channel.category.id
    info += f"{ctx.guild.id}\n{channelId}\n{cat}"
    file = open('serverInfo.txt', 'w')
    file.write(info)
    file.close()

@bot.command()
async def info(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        return
    info = open('serverInfo.txt')
    lines = info.read().splitlines()
    info.close()
    if(len(lines) == 0):
        await ctx.send("info is null")
        return
    embed = discord.Embed(title="Info", description=f"Guild: {lines[0]}\nVoice channel: <#{lines[1]}>({lines[1]})\nCategory: <#{lines[2]}>")
    await ctx.send(embed=embed)


@bot.event
async def on_voice_state_update(member, before, after):
    info = open('serverInfo.txt')
    lines = info.read().splitlines()
    info.close()
    guild = member.guild
    if not before.channel and after.channel and after.channel.id == int(lines[1]):
        cat = discord.utils.get(guild.categories, id=int(lines[2]))
        voiceChannel = await guild.create_voice_channel(f"{member} channel", category=cat)
        await member.move_to(voiceChannel)
        return
    if before.channel is not None and after.channel is None and before.channel.category.id == int(lines[2]) and before.channel.id != int(lines[1]):
        members = before.channel.members
        count = 0;
        for member in members:
            count += 1
        if count != 0:
            return
        channel = before.channel
        if type(channel) != discord.channel.VoiceChannel or channel is None:
            print("No channel found!")
            return
        await channel.delete()


token = open('token.txt', 'r').readline()
bot.run(token)