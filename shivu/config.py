class Config(object):
    LOGGER = True

    # Bot Owner & Sudo Users
    OWNER_ID = 8156600797
    sudo_users = [7640076990, 7756901810, 8156600797]

    # Bot Credentials
    GROUP_ID = -1002499806698
    TOKEN = "8136650512:AAFC8c8225hPO_q2AFKtZtADMjCRryF1ZJU"
    mongo_url = "mongodb+srv://Naruto777:hinata654@naruto77.e14xiqc.mongodb.net/?retryWrites=true&w=majority"

    # Bot Settings
    PHOTO_URL = [
        "https://graph.org/file/09e83a1d89aceabd480c5-2afc46a31083fe23f2.jpg",
        "https://graph.org/file/0aa659508c1add9ae4c86-2b335aa5262b7b64d2.jpg"
    ]
    SUPPORT_CHAT = "Anime_Circle_Club"
    UPDATE_CHAT = "Waifu_Chan_Bot_updates"
    BOT_USERNAME = "@Waifu_Chan_Robot"
    CHARA_CHANNEL_ID = -1002646820042  # Channel ID should be an integer

    # API Credentials
    api_id = 28159105
    api_hash = "a0936ddf210a7e091e19947c7dc70c91"


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
