import discord
import json
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
    guild = bot.get_guild(691182902633037834) #temporary

    with open("main_canals.json", "r") as myFile:
        channels_json = myFile.read()
    if(len(channels_json) == 0):
        print("main_canals.json is null")
        return

    channels = json.loads(channels_json)
    updatedChannels = []

    for channel in channels[0]:
        checkedChannel = discord.utils.get(guild.channels, id=int(channel))
        if(int(len(checkedChannel.members)) != 0):
            updatedChannels.append(channel)
            continue
        if type(checkedChannel) != discord.channel.VoiceChannel or checkedChannel is None:
            print("No channel found!")
        else:
            await channel.delete()

    channels_json = json.dumps(updatedChannels)
    with open("main_canals.json", "w") as myFile:
        myFile.write(channels_json)


def main():
  return "Your bot is alive!"

@bot.command()
async def reg(ctx, channelId):#need to edit
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
async def info(ctx):#need to edit
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
async def on_voice_state_update(member, before, after):#need to edit
    info = open('serverInfo.txt')
    lines = info.read().splitlines()
    info.close()
    guild = member.guild
    if not before.channel and after.channel and after.channel.id == int(lines[1]):
        cat = discord.utils.get(guild.categories, id=int(lines[2]))
        voiceChannel = await guild.create_voice_channel(f"{member} channel", category=cat)
        await member.move_to(voiceChannel)
        channelsFile = open('channels.txt')
        info = channelsFile.read()
        if info != "":
            info += "\n"
        info += f"{voiceChannel.id};{member.id}"
        channelsFile.close()
        file = open('channels.txt', 'w')
        file.write(info)
        file.close()
        return
    if before.channel is not None and after.channel is None and before.channel.category.id == int(lines[2]) and before.channel.id != int(lines[1]):
        isTrue = False
        info = open('channels.txt')
        newInfo = ""
        lines = info.read().splitlines()
        info.close()
        for line in lines:
            words = line.split(";")
            if int(before.channel.id) == int(words[0]):
                isTrue = True
            else:
                if newInfo != "":
                    newInfo += "\n"
                newInfo += line
        if not isTrue:
            return
        members = before.channel.members
        if len(members) != 0:
            return
        channel = before.channel
        if type(channel) != discord.channel.VoiceChannel or channel is None:
            print("No channel found!")
            return
        await channel.delete()
        file = open('channels.txt', 'w')
        file.write(newInfo)
        file.close()



token = open('token.txt', 'r').readline()
bot.run(token)
