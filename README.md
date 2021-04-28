# Twitter-Block-Bot
## Purpose
Traditional celebrities, e-celebs and neo-lib corporations virtue signal on Twitter quite often, so this bot is a solution to all the morons that fall for this garbagee (those users that hit like on said virtue-signalling tweets) or for the automated bots that inflate like counts.
### Current functionality:
A Python bot that opens a list of tweets and blocks the users that liked them.
### How it works:
The bot logs into your account in an object of type `BlockBot`. You then make this object load up the list of tweets in a text file, and then it proceeds to block every account that liked these tweets.
### How to use:
- Clone the repo and add a `.env` file to the root. Put into it:
```
USER_NAME=yourtwitterusername
PASS=yourtwitterpassword
```
- Your Twitter account must have 2-factor authenticate turned off.
- Locate `tweets.txt` which is either in the same folder as `twitter_block_bot.py` or in the sub-folder `Scripts & Notebooks` as both will work.
- Insert into this file each tweet you want (for blocking each user that liked it) on a new line. You can get the tweet link by clicking on "Copy link to tweet."
- You can select that number of accounts to block in each tweet in the variable `num_accs`, but note that Twitter only loads a couple of tweets at a time, so by default this is set to 1000, which will block as many accounts that get loaded.
- Or run and configure `Notebook-Twitter Block Bot.ipynb` to your liking.
- You will need the Chrome webdriver which you can pick up at https://sites.google.com/a/chromium.org/chromedriver/downloads and you will need to either set the PATH variable to where your own chromedriver.exe is, or alternatively place your webdriver in `C:\Program Files (x86)\chromedriver_win32\` as I have done.
#### Note:
- Twitter only loads a couple of accounts at one time. So you can input a large number of accounts to block, but the bot will finish long before this limit is reached as Twitter delays loading more accounts by some minutes.
- You may get rate-limited by Twitter for multiple API calls in a row. You just need to wait some minutes for it to reset, then you can continue blocking.
### Python modules required:
selenium, dotenv, time, os.

selenium and dotenv will likely need to be installed with pip
time and os are in the standard library (I think)
