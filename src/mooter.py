from bs4 import BeautifulSoup
import urllib.request


url = "https://twitter.com/realDonaldTrump"


def main():
    with urllib.request.urlopen(url) as response:
        soup = BeautifulSoup(response.read(), 'html.parser')

        tweets = soup.find_all("div", {"class": "js-tweet-text-container"})
        for tweet in tweets:
            tweet_text = parse_tweet(tweet)
            print(tweet_text.replace("\n", ". "))


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
