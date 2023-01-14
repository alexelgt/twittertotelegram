# twittertotelegram
# Copyright (C) 2023 Alexelgt

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

news_info = {
    "2839430431" :{
        "channel_id": -1001790033099,
        "screen_name": "PokemonGoApp"
    },
    "849344094681870336": {
        "channel_id": -1001609741706,
        "screen_name": "NianticHelp"
    },
    "1163205412650475520": {
        "channel_id": -1001516322334,
        "screen_name": "poke_miners"
    },
    "840992778020630531": {
        "channel_id": -1001632232660,
        "screen_name": "LeekDuck"
    },
    # "1024025263586172928": {
    #     "channel_id": -1001740184540,
    #     "screen_name": "LEGENDSLima"
    # },
    "1584975646412996619": {
        "channel_id": -1001740184540,
        "screen_name": "MikoGraphicsPE"
    },
    "1450170589071626243": {
        "channel_id": -1001637695143,
        "screen_name": "PikminBloom"
    }
}

SCRIPT_FOLDER = os.path.dirname(__file__) + "/"

config_info = configparser.RawConfigParser()
config_info.read(SCRIPT_FOLDER + "config.ini")

BOT_TOKEN = config_info["bot"]["token"]

BEARER_TOKEN = config_info["twitter"]["bearer_token"]
