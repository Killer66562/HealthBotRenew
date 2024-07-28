from discord.ext.commands import Bot
from discord import Intents, Status

from cogs import SurveyCog


health_bot = Bot(command_prefix="health~", description="智能健康管家", intents=Intents.all())

survey_cog = SurveyCog()

@health_bot.event
async def on_ready():
    await health_bot.add_cog(survey_cog)
    await health_bot.tree.sync()
    await health_bot.change_presence(status=Status.online)

health_bot.run(token="MTI2NjM4MzIyNDg4ODYyMzE1NQ.GWw_pp.Ed4PMVGx0YOEY7qb5x0W6H0ujnMfOtK7KUOfgM", reconnect=True)