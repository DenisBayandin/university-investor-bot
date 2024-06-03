from decouple import config


bot_token = config("BOT_TOKEN", cast=str)
tinkoff_token = config("TINKOFF_TOKEN", cast=str)
