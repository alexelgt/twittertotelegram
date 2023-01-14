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

import tweepy

import twittertotelegram.supportmethods as support

from twittertotelegram.config import BEARER_TOKEN

tweet_id = 1598035205310513152

def main():
    client = tweepy.Client(BEARER_TOKEN)

    response = client.get_tweets(tweet_id, tweet_fields=["author_id", "in_reply_to_user_id", "referenced_tweets", "entities"], expansions=["attachments.media_keys"], media_fields=["type", "url", "variants"])

    tweet = {
        "data": dict(response.data[0]),
        "includes": response.includes
    }

    print(tweet)

    support.process_tweet(tweet)

if __name__ == "__main__":
    main()
