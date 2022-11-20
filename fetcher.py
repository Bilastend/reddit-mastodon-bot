import praw
import statics
import random

reddit = praw.Reddit(
    client_id=statics.client_id,
    client_secret=statics.client_secret,
    user_agent=statics.user_agent
)


def fetch() -> tuple[str, str]:
    subreddit = reddit.subreddit("wholesomememes")
    submissions = subreddit.hot(limit=75)
    submissions = [
        x for x in submissions if not x.is_self and x.upvote_ratio >= 0.9]
    submission = random.choice(submissions)
    return (submission.title, submission.url)
