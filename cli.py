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

import tweepy

import twittertotelegram.sql as sql

import twittertotelegram.supportmethods as support

from twittertotelegram.config import news_info, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def main():
    auth = tweepy.OAuth1UserHandler(APP_KEY, APP_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    app = tweepy.API(auth, wait_on_rate_limit=True)

    for screen_name in news_info:
        since_id_old = sql.get_since_id(screen_name)

        tweets = support.get_tweets(app, screen_name, since_id=since_id_old)

        try:
            # Expected Exception if len(tweets) == 0
            since_id_new = tweets[0].id

            for tweet in tweets[::-1]:
                support.process_tweet(tweet)

            if since_id_new != since_id_old:
                sql.update_since_id(screen_name, since_id_new)
        except IndexError:
            pass

if __name__ == "__main__":
    main()
