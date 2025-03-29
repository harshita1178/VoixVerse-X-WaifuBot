class Config(object):
    LOGGER = True
    # Get this value from my.telegram.org/apps
    OWNER_ID = "6675050163"
    sudo_users = "8156600797", "7640076990", "7756901810"
    GROUP_ID = -1002640379822
    TOKEN = "8136650512:AAFC8c8225hPO_q2AFKtZtADMjCRryF1ZJU"  # Updated Token
    mongo_url = "mongodb+srv://walkrock:<supermanxxxx>@sunny.vu6keb7.mongodb.net/?retryWrites=true&w=majority&appName=sunny"
    PHOTO_URL = "https://files.catbox.moe/0nb1p7.jpg"
    SUPPORT_CHAT = "blade_x_support"
    UPDATE_CHAT = "blade_x_community"
    BOT_USERNAME = "Devine_wifu_bot"
    CHARA_CHANNEL_ID = "-4705079232"  # Updated Character Channel
    api_id = 28159105
    api_hash = "a0936ddf210a7e091e19947c7dc70c91"
class Production(Config):
    LOGGER = True
class Development(Config):
    LOGGER = True
