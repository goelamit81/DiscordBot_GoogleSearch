import discord
from discord.ext import commands

import environment as env
import google_search as gs
import database as db

################################################################################################

bot = commands.Bot(command_prefix='!')

################################################################################################

@bot.command(name='google', help='Return top five result from google search')
async def bot_google_search(ctx, *args):

    # validate user input
    if not args:
        await ctx.send(env.INPUT_REQUIRED_MSG)
    else:
        search_keyword = ' '.join(args)
        # validate if input is less than or equal to 255 characters
        if len(search_keyword) > env.SEARCH_KEY_MAX_LENGTH:
            await ctx.send(env.MAX_INPUT_LENGTH_MSG)
        else:
            # create entry in database
            db.create_search_history(ctx.message.author.id, search_keyword)
            # get result from google api
            results = gs.google_search(search_keyword)
            if not results:
                await ctx.send(env.NO_SEARCH_RESULT_MSG)
            for result in results:
                embed = discord.Embed(
                    title=result.get('title'),
                    url=result.get('link'),
                    description=result.get('description'),
                    color=discord.Color.purple()
                )

                await ctx.send(embed=embed)

################################################################################################

@bot.command(name='recent', help='Return related search history')
async def bot_search_history(ctx, *args):

    # validate user input
    if not args:
        await ctx.send(env.INPUT_REQUIRED_MSG)
    else:
        search_keyword = ' '.join(args)
        # validate if input is less than or equal to 255 characters
        if len(search_keyword) > env.SEARCH_KEY_MAX_LENGTH:
            await ctx.send(env.MAX_INPUT_LENGTH_MSG)
        else:
            # search history in database
            search_history = db.get_search_history(ctx.message.author.id, search_keyword)
            search_history = [x[0] for x in search_history]
            if len(search_history) > 0:
                search_history = ['**Search History**'] + search_history
            else:
                search_history = ['**No Search History Found**']

            await ctx.send('\n'.join(search_history))

################################################################################################

@bot_google_search.error
@bot_search_history.error
async def bot_error(ctx, error):

    await ctx.send('Error - {}'.format(error))

################################################################################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

################################################################################################

if __name__ == '__main__':

    db.setup_search_history_table()
    bot.run(env.DISCORD_TOKEN)

################################################################################################