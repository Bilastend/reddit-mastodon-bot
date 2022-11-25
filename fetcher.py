import praw
import statics
import statistics
import random

from os.path import exists
reddit = praw.Reddit(
    client_id=statics.client_id,
    client_secret=statics.client_secret,
    user_agent=statics.user_agent
)

image_links = []


def fetch() -> tuple[str, str]:
    subreddit = reddit.subreddit(statics.subreddit)
    submissions = [
        x for x in subreddit.hot(limit=250) if not x.is_self and x.upvote_ratio >= 0.9 and x.url not in image_links]
    # I have no idea what I'm doing here but it sorts out posts that don't have an high enough score at the moment
    min_score = statistics.mean([x.score for x in submissions])*0.23
    submissions = [x for x in submissions if x.score >= min_score]
    submission = random.choice(submissions)
    image_links.append(submission.url)
    print(submission.url)
    return (submission.title, submission.url)


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
