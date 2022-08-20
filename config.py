# twittertotelegram
# Copyright (C) 2022 Alexelgt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import configparser

news_info = [
    {
        "screen_name": "PokemonGoApp",
        "channel_id": -1001790033099
    },
    {
        "screen_name": "NianticHelp",
        "channel_id": -1001609741706
    },
    {
        "screen_name": "poke_miners",
        "channel_id": -1001516322334
    },
    {
        "screen_name": "LeekDuck",
        "channel_id": -1001632232660
    },
    {
        "screen_name": "LEGENDSLima",
        "channel_id": -1001740184540
    },
    {
        "screen_name": "PikminBloom",
        "channel_id": -1001637695143
    },
]

SCRIPT_FOLDER = os.path.dirname(__file__) + "/"

config_info = configparser.RawConfigParser()
config_info.read(SCRIPT_FOLDER + "config.ini")

BOT_TOKEN = config_info["bot"]["token"]

SQL_USER = config_info["database"]["user"]
SQL_PASSWORD = config_info["database"]["password"]
SQL_DATABASE = config_info["database"]["name"]

APP_KEY = config_info["twitter"]["app_key"]
APP_SECRET = config_info["twitter"]["app_secret"]

OAUTH_TOKEN = config_info["twitter"]["oauth_token"]
OAUTH_TOKEN_SECRET = config_info["twitter"]["oauth_token_secret"]