#Copyright 2016 Inversebit/Alex M
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from bs4 import BeautifulSoup
from google.cloud import language
import urllib.request


def main():

    person = get_person_to_spy()
    url = "https://twitter.com/" + person

    with urllib.request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')
        print_name(soup)
        print_tweets(soup)


def get_person_to_spy():
    return input("On whom shall we spy? ")


def print_name(soup):
    name = soup.find("a", {"class": "ProfileHeaderCard-screennameLink"}).span.contents[0]
    print("\n\nThis is what @" + name + " has to say today:\n")


def print_tweets(soup):
    tweets = soup.find_all("div", {"class": "js-tweet-text-container"})
    for tweet in tweets:
        tweet_text = parse_tweet(tweet)
        print(tweet_text.replace("\n", ". "))

        analyze_and_print_sentiment(tweet_text)


def analyze_and_print_sentiment(tweet_text):
    sentiment_client = language.Client()
    doc = sentiment_client.document_from_text(tweet_text.replace("\n", ". "))
    sentiment = doc.analyze_sentiment()
    print("This tweet was " + ("happy" if sentiment.polarity > 0 else "mean"))


def parse_tweet(tweet):
    tweet_text = ""
    for elem in tweet.p.contents:
        tweet_text += remove_links(elem)

    return tweet_text


def remove_links(tweet_content):
    res = ""
    if tweet_content.name == 'a':
        if len(tweet_content.contents) == 2:
            res += " "
            res += tweet_content.contents[1].contents[0]
    else:
        res += tweet_content

    return res


if __name__ == "__main__":
    print(">> Init mooter")
    main()
    print(">> Mooter finished")
