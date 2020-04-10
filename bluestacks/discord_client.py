import discord

import environment as env

################################################################################################

client = discord.Client()

################################################################################################

# Setup a client for general communication. Only expectation here is that we response Hey if someone says hi
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself if bot send message then dont send anything
    if message.author == client.user:
        return
    # if we get a message like hi, HI, Hi, hello, Hello, HELLO response back with Hey
    if message.content.lower() in env.RECV_GREETING:
        await message.channel.send(env.SEND_GREETING)

if __name__ == '__main__':
    client.run(env.DISCORD_TOKEN)

################################################################################################