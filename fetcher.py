import asyncpraw
import statics
import random

reddit = asyncpraw.Reddit(
    client_id=statics.client_id,
    client_secret=statics.client_secret,
    user_agent=statics.user_agent
)

async def fetch() -> tuple[str,str]:
    subreddit = await reddit.subreddit("wholesomememes")
    submissions = subreddit.hot(limit=50)
    submissions = [x async for x in submissions if not x.is_self and x.upvote_ratio >= 0.8]
    submission = random.choice(submissions)
    return (submission.title, submission.url)