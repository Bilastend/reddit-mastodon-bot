import asyncpraw
import statics
import statistics
import random

from os.path import exists

image_links = []


async def fetch() -> tuple[str, str]:
    global image_links
    async with asyncpraw.Reddit(
            client_id=statics.client_id, client_secret=statics.client_secret, user_agent=statics.user_agent) as reddit:
        subreddit = await reddit.subreddit(statics.subreddit)
        raw_submissions = []
        async for submission in subreddit.top(time_filter="all", limit=500):
            raw_submissions.append(submission)
        submissions = [
            x for x in raw_submissions
            if not x.is_self and x.upvote_ratio >= 0.9 and x.url
            not in image_links and "imgur"
            not in x.url and ".gif" not in x.url and "v.redd.it" not in x.url]
        min_score = statistics.median([x.score for x in submissions])
        cleaned_submissions = [x for x in submissions if x.score >= min_score]
        submission = random.choice(cleaned_submissions)
        image_links.append(submission.url)
        print(submission.url)
        name = ''
        if (submission.author == None):
            name = '[Deleted user]'
        else:
            name = submission.author.name
        return (submission.title, submission.url, name)


def save_image_links():
    global image_links
    with open('image_links.txt', 'w') as f:
        for line in image_links:
            f.write("%s\n" % line)
    print('Saving completed.')


def load_image_links():
    if not exists('image_links.txt'):
        return
    global image_links
    with open('image_links.txt') as f:
        image_links = f.read().splitlines()
    print('Loading completed.')
