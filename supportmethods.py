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

import requests

from twittertotelegram.regex import TWITTER_USERNAME_REGEX

from twittertotelegram.config import BOT_TOKEN, news_info

TWEET_URL = "https://twitter.com/{}/status/{}"

def utf_16_len(text):
    return int(len(text.encode("utf-16-le")) / 2)

def send_tweet(screen_name, tweet_text):
    if screen_name == "LEGENDSLima":
        if any([x in tweet_text for x in ("🇺🇸", "🇪🇸", "🇫🇷")]):
            return ("🇺🇸" in tweet_text) or ("🇪🇸" in tweet_text)

        return True

    return True

def send_text_message(chat_id, output_text, link_entities=None):
    if link_entities is not None:
        link_entities = json.dumps(link_entities)

    try:
        if output_text is not None:
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
        if output_text is not None:
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

def update_link_entities(link_entities, link_text, output_text, tweet_url):
    output_text_len = utf_16_len(output_text)
    link_text_len = utf_16_len(link_text)

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

def remove_media_link(tweet_text, tweet_entities):
    try:
        for entity in tweet_entities["urls"]:
            try:
                entity["media_key"]
                return tweet_text.replace(entity["url"], "")
            except KeyError:
                pass
    except:
        pass

    return tweet_text

def get_tweet_type_id(tweet, tweet_type):
    try:
        for referenced_tweet in tweet["data"]["referenced_tweets"]:
            if referenced_tweet["type"] == tweet_type:
                return referenced_tweet["id"]
    except:
        pass

    return None

def get_quoted_tweet_link(tweet):
    try:
        quoted_id = get_tweet_type_id(tweet, "quoted")

        if quoted_id is not None:
            for url_info in tweet["data"]["entities"]["urls"]:
                if ("twitter.com" in url_info["expanded_url"]) and (quoted_id in url_info["expanded_url"]):
                    return url_info["url"]
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

                # Remove media link
                output_text = remove_media_link(tweet["data"]["text"], tweet["data"]["entities"])

                # Remove quote link
                quoted_tweet_link = get_quoted_tweet_link(tweet)

                if quoted_tweet_link is not None:
                    output_text = output_text.replace(quoted_tweet_link, "")

                # Clean extra spaces
                try:
                    output_text = output_text.strip()
                except:
                    pass

                # Tweet link
                link_text = "🔗 Tweet link"
                output_text = output_text.replace("&amp;", "&") + f"\n\n{link_text}"

                link_entities = []

                update_username_entities(link_entities, output_text)

                tweet_url = TWEET_URL.format(screen_name, tweet["data"]["id"])

                update_link_entities(link_entities, link_text, output_text, tweet_url)

                # Reply Tweet
                if in_reply_to_user_id is not None:
                    link_text = "📩 In reply to"
                    output_text += f" | {link_text}"

                    reply_tweet_url = TWEET_URL.format(screen_name, get_tweet_type_id(tweet, "replied_to"))

                    update_link_entities(link_entities, link_text, output_text, reply_tweet_url)

                # Quote tweet
                if quoted_tweet_link is not None:
                    link_text = "💬 Quoted tweet"
                    output_text += f" | {link_text}"

                    update_link_entities(link_entities, link_text, output_text, quoted_tweet_link)

                try:
                    # Expected Exception if Tweet does not have media
                    media_info = get_media_info(tweet["includes"]["media"])

                    send_media_group_message(channel_id, output_text, media_info, link_entities=link_entities)
                except KeyError:
                    # If it's not media
                    send_text_message(channel_id, output_text, link_entities=link_entities)
    except:
        pass
