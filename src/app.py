from discord.ext.commands import Bot
from discord import Intents, Status

from cogs import SurveyCog

from dotenv import load_dotenv

import os


load_dotenv()

health_bot = Bot(command_prefix="health~", description="智能健康管家", intents=Intents.all())

survey_cog = SurveyCog()

@health_bot.event
async def on_ready():
    await health_bot.add_cog(survey_cog)
    await health_bot.tree.sync()
    await health_bot.change_presence(status=Status.online)

health_bot.run(token=os.getenv("TOKEN"), reconnect=True)