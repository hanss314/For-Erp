import discord, asyncio, ast

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith('!embed'):
        params = message.content.split(' ')
        to_embed = discord.Embed(type='rich')
        tup = ast.literal_eval(params[1])
        to_embed.colour=int(tup[2])+256*int(tup[1])+256*256*int(tup[0])
        to_embed.title = params[2]
        to_embed.description = ' '.join(params[3:])
        await client.send_message(message.channel,'',embed=to_embed)


client.run('MzAyNjkxODI5MTcyNjY2MzY4.DAF4Cw.WIk-QzvdTgM7M-7O8M-6rMzSBCE')
