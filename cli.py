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

import json

import tweepy

import twittertotelegram.supportmethods as support

from twittertotelegram.config import news_info, BEARER_TOKEN

class Streaming(tweepy.StreamingClient):
    def on_data(self, raw_data):
        tweet = json.loads(raw_data)

        support.process_tweet(tweet)

def main():
    streamer = Streaming(BEARER_TOKEN)

    # try:
    #     for rule in streamer.get_rules().data:
    #         streamer.delete_rules(ids=rule.id)
    # except TypeError:
    #     pass

    # streamer.add_rules([tweepy.StreamRule(f'from:{news_info[twitter_id]["screen_name"]} -is:retweet') for twitter_id in news_info])

    # print(streamer.get_rules())

    streamer.filter(tweet_fields=["author_id", "in_reply_to_user_id", "referenced_tweets", "entities"], expansions=["attachments.media_keys"], media_fields=["type", "url", "variants"])

if __name__ == "__main__":
    main()
