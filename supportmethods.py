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

import json

import requests

from twittertotelegram.regex import TWITTER_USERNAME_REGEX

from twittertotelegram.config import BOT_TOKEN, news_info

def utf_16_len(text):
    return int(len(text.encode("utf-16-le")) / 2)

def send_tweet(screen_name, tweet_text):
    if screen_name == "LEGENDSLima":
        if any([x in tweet_text for x in ("🇺🇸", "🇪🇸", "🇫🇷")]):
            return ("🇺🇸" in tweet_text) or ("🇪🇸" in tweet_text)

        return True

    return True

def get_tweets(app, account, since_id=None, number_tweets=80):
    tweets = tweepy.Cursor(app.user_timeline, 
        screen_name=account, 
        tweet_mode="extended",
        since_id=since_id,
        exclude_replies=False
    ).items(number_tweets)

    return list(tweets)

def send_text_message(chat_id, output_text, link_entities=None):
    if link_entities is not None:
        link_entities = json.dumps(link_entities)

    try:
        if output_text != None:
            message_sent = requests.post(
                url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={
                    "chat_id": chat_id,
                    "text": output_text,
                    "disable_web_page_preview": True,
                    "entities": link_entities
                }
            ).json()["result"]

            return message_sent
        return
    except:
        return

def send_media_group_message(chat_id, output_text, media_info, link_entities=None):
    try:
        if output_text != None:
            images_info = [{"type": media["type"], "media": media["media_url"]} for media in media_info]
            images_info[0]["caption"] = output_text
            images_info[0]["caption_entities"] = link_entities

            message_sent = requests.post(
                url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMediaGroup",
                data={
                    "chat_id": chat_id,
                    "media": json.dumps(images_info)
                }
            ).json()["result"]

            return message_sent
        return
    except:
        return

def update_username_entities(link_entities, output_text):
    username_matches = [(m.span()) for m in TWITTER_USERNAME_REGEX.finditer(output_text)]

    for username_match in username_matches:
        output_text_before = output_text[:username_match[0]]
        username_text = output_text[username_match[0]:username_match[1]]

        output_text_before_len = utf_16_len(output_text_before)
        username_text_len = utf_16_len(username_text)

        username_url = f"https://twitter.com/{username_text[1:]}"

        link_entities.extend([
            {"type": "text_link", "offset": output_text_before_len, "length": username_text_len, "url": username_url}
        ])

def update_link_entities(link_entities, link_text, output_text, screen_name, tweet_id):
    output_text_len = utf_16_len(output_text)
    link_text_len = utf_16_len(link_text)

    tweet_url = f"https://twitter.com/{screen_name}/status/{tweet_id}"

    link_entities.extend([
        {"type": "text_link", "offset": output_text_len - link_text_len, "length": link_text_len, "url": tweet_url},
        {"type": "bold", "offset": output_text_len - link_text_len, "length": link_text_len}
    ])

def get_video_url(video_variants):
    for video_variant in video_variants:
        if video_variant["content_type"] != "application/x-mpegURL":
            return video_variant["url"]

    return None

def get_media_info(tweet_media_entities):
    media_info = []

    for media in tweet_media_entities:
        try:
            if media["type"] == "photo":
                media_info.append(
                    {
                        "type": "photo",
                        "media_url": media["url"]
                    }
                )
            elif media["type"] == "video":
                video_url = get_video_url(media["variants"])

                if video_url:
                    media_info.append(
                        {
                            "type": "video",
                            "media_url": video_url
                        }
                    )
        except:
            pass

    return media_info

# Should not be needed
# def check_tweet(tweet):
#     try:
#         for referenced_tweet in tweet["data"]["referenced_tweets"]:
#             if referenced_tweet["type"] == "retweeted":
#                 return False

#         return True
#     except:
#         return True

def get_replied_to_id(tweet):
    try:
        for referenced_tweet in tweet["data"]["referenced_tweets"]:
            if referenced_tweet["type"] == "replied_to":
                return referenced_tweet["id"]
    except:
        pass

    return None

def process_tweet(tweet):
    try:
        try:
            in_reply_to_user_id = tweet["data"]["in_reply_to_user_id"]
        except:
            in_reply_to_user_id = None

        if (in_reply_to_user_id is None) or (in_reply_to_user_id == tweet["data"]["author_id"]):
            screen_name = news_info[tweet["data"]["author_id"]]["screen_name"]
            channel_id = news_info[tweet["data"]["author_id"]]["channel_id"]

            if send_tweet(screen_name, tweet["data"]["text"]):
                # Original Tweet

                # Remove media link from output text
                try:
                    output_text = tweet["data"]["text"].replace(tweet["includes"]["media"][0]["url"], "")
                except KeyError:
                    output_text = tweet["data"]["text"]

                link_text = "🔗 Tweet link"
                output_text = output_text.replace("&amp;", "&") + f"\n\n{link_text}"

                link_entities = []

                update_username_entities(link_entities, output_text)

                update_link_entities(link_entities, link_text, output_text, screen_name, tweet["data"]["id"])

                # Reply Tweet
                if in_reply_to_user_id is not None:
                    link_text = "📩 In reply to"
                    output_text += f" | {link_text}"

                    update_link_entities(link_entities, link_text, output_text, screen_name, get_replied_to_id(tweet))

                try:
                    # Expected Exception if Tweet does not have media
                    media_info = get_media_info(tweet["includes"]["media"])

                    send_media_group_message(channel_id, output_text, media_info, link_entities=link_entities)
                except KeyError:
                    # If it's not media
                    send_text_message(channel_id, output_text, link_entities=link_entities)
    except:
        pass