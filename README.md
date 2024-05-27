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

    open_ai_key = "OpenAI API key" # Skip this line if you don't want to use AI

You also need different libraries. In my case, Arch btw, install them like this:

    # pacman -S --needed enchant libvoikko aspell aspell-en
    
Run your Bot

    $ python main.py

## Alt-Text

It is possible to provide alt text with the posts.
There a three ways to do this:
- Manual
- AI (an OpenAI API key is needed)
- OCR (local Tesseract)

Todo it manually, just create a file called 'alt_text.txt' in the source directory and write your alt text into the file. If the file is present the alt text will be added to the image and the file will be deleted. This means in the default case you have two hours to provide a description. You just have to check the console output for the next image. 

If the file does not exist the bot will use AI, if an API key is provided in statics.py.
Tesseract is used as a fallback, in case no API key is provided or it simply fails e.g. for quota reasons.

Before adding the description to the post it will check if the percentage of proper english words is over a certain threshold to make sure that the description generated makes sense, if the check failes no alt text will be provided.
    
