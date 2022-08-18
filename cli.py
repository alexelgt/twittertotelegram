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

from time import sleep

import twittertotelegram.sql as sql

import twittertotelegram.supportmethods as support

from twittertotelegram.config import news_info, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def main():
    auth = tweepy.OAuth1UserHandler(APP_KEY, APP_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    app = tweepy.API(auth, wait_on_rate_limit=True)

    for news_element in news_info:
        since_id_old = sql.get_since_id(news_element["screen_name"])

        tweets = support.get_tweets(app, news_element["screen_name"], since_id=since_id_old)

        try:
            # Expected Exception if len(tweets) == 0
            since_id_new = tweets[0].id

            for tweet in tweets[::-1]:
                try:
                    try:
                        # Expected Exception if it's not a RT (RTs should not be sent)
                        tweet.retweeted_status
                    except AttributeError:
                        # If it's not a RT
                        if tweet.in_reply_to_screen_name in [news_element["screen_name"], None]:
                            if support.send_tweet(news_element["screen_name"], tweet.full_text):
                                # Original Tweet
                                link_text = "🔗 Tweet link"
                                output_text = tweet.full_text.replace("&amp;", "&") + "\n\n{}".format(link_text)

                                link_entities = []

                                support.update_username_entities(link_entities, output_text)

                                support.update_link_entities(link_entities, link_text, output_text, news_element["screen_name"], tweet.id)

                                # Reply Tweet
                                if tweet.in_reply_to_screen_name == news_element["screen_name"]:
                                    link_text = "📩 In reply to"
                                    output_text += " | {}".format(link_text)

                                    support.update_link_entities(link_entities, link_text, output_text, news_element["screen_name"], tweet.in_reply_to_status_id)

                                try:
                                    # Expected Exception if Tweet does not have media
                                    media_info = support.get_media_info(tweet.extended_entities["media"])

                                    support.send_media_group_message(news_element["channel_id"], output_text, media_info, link_entities=link_entities)
                                except AttributeError:
                                    # If it's not media
                                    support.send_text_message(news_element["channel_id"], output_text, link_entities=link_entities)

                                sleep(1)
                except:
                    pass

            if since_id_new != since_id_old:
                sql.update_since_id(news_element["screen_name"], since_id_new)
        except IndexError:
            pass

if __name__ == "__main__":
    main()
