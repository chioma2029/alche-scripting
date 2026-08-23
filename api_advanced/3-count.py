#!/usr/bin/python3
"""Recursively count keyword occurrences in a subreddit's hot titles."""
import requests


def count_words(subreddit, word_list, counts=None, after=None):
    """Print a sorted count of keywords found in hot post titles."""
    if counts is None:
        counts = {}
        for word in word_list:
            counts[word.lower()] = 0

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:subreddit-checker:v1.0"}
    params = {"limit": 100, "after": after}
    response = requests.get(url, headers=headers, params=params,
                             allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get("data")
    posts = data.get("children")

    for post in posts:
        title = post.get("data").get("title").lower()
        for token in title.split():
            clean = token.strip(".,!?;:_\"'()[]{}")
            if clean in counts:
                counts[clean] += 1

    after = data.get("after")
    if after is not None:
        return count_words(subreddit, word_list, counts, after)

    print_counts(counts)


def print_counts(counts):
    """Print word counts sorted by count desc, then alphabetically."""
    items = [(word, n) for word, n in counts.items() if n > 0]
    items.sort(key=lambda pair: (-pair[1], pair[0]))
    for word, n in items:
        print("{}: {}".format(word, n))
