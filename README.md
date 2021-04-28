# Twitter-Block-Bot
### Current functionality:
A Python bot that opens a tweet and blocks the users that liked it.
### How it works:
The bot loads up the tweet in question, logs into your account, and then proceeds to block every account that liked this tweet. Useful for mass blocking bot accounts, or other cringe accounts.
### How to use:
- Clone the repo and add a `.env` file to the root. Put into it:
```
USER_NAME=yourtwitterusername
PASS=yourtwitterpassword
```
- Your Twitter account must have 2-factor authenticate turned off.
- Run either `twitter_block_bot.py` and insert the tweet URL (click on "Copy link to tweet" in the tweet menu), and the number of accounts to block,
- or run and configure `Notebook-Twitter Block Bot.ipynb` to your liking.
- You will need the Chrome webdriver which you can pick up at https://sites.google.com/a/chromium.org/chromedriver/downloads and you will need to either set the PATH variable to where your own chromedriver.exe is, or alternatively place your webdriver in `C:\Program Files (x86)\chromedriver_win32\` as I have done.
#### Note:
Twitter only loads a couple of accounts at one time, so you can input a large number of accounts to block, but the bot will finish much before as Twitter delays loading more accounts by some minutes.
### Python modules required:
selenium, dotenv, time, os.

selenium and dotenv will likely need to be installed with pip
