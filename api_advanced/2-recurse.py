#!/usr/bin/python3
"""Recursively query the Reddit API for all hot post titles."""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Return a list of titles of all hot posts in a subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:subreddit-checker:v1.0"}
    params = {"limit": 100, "after": after}
    response = requests.get(url, headers=headers, params=params,
                             allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get("data")
    posts = data.get("children")

    for post in posts:
        hot_list.append(post.get("data").get("title"))

    after = data.get("after")
    if after is None:
        return hot_list

    return recurse(subreddit, hot_list, after)
