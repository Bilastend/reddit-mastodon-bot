# Reddit Mastodon Bot

This is a bot that fetches an image from a specific subreddit to post on Mastodon every hour.
While the scheduler waits a full hour to post the image to Mastodon, it is already being processed in the background. This way, there is no extra delay, as image processing can sometimes take up to a few minutes.

Currently in use for: https://botsin.space/web/@wholesomememes

## How to run

Clone the repository and cd into it.

    $ git clone https://github.com/Bilastend/wholesome
    $ cd wholesome

Create a virtual environment to run the bot *(recommended)*.

    $ python -m venv venv
    $ source venv/bin/activate

Install the packages in [requirements.txt](requirements.txt) using pip.

    $ pip install -r requirements.txt
    
Create a file called **statics.py** in the source directory of this repo and add the following lines to it:

    client_id = "The client id of your reddit Application"
    
    client_secret = "The client secret of your reddit Application"
    
    access_token = "The access token to your Mastodon application"

    api_base_url = "The url of the bot instance for example https://botsin.space"
    
    user_agent = "The user agent for Reddits API in this format: <platform>:<app ID>:<version string> (by /u/<reddit username>)"
    
    subreddit = "The name of your subreddit"
    
Run your Bot

    $ python main.py

## Alt-Text

It is possible to provide Alt-Text with this bot but that has to be done manually. Todo so, just create a file called 'alt_text.txt' in the source directory and write an alt-text into the file. If the file is present the alt-text will be added to the image and the file will be deleted. If it does not exist there is no alt-text. This means in the default case you have one hour to provide the alt-text. You just have to check the console output for the next image.
    
