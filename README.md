# Twitter-Block-Bot
### Current functionality:
A Python bot that opens a tweet and blocks the users that liked it.
### How to use:
- Clone the repo and add a .env to the root. Put in it:
```
USER_NAME=yourtwitterusername
PASS=yourtwitterpassword
```
- Run either `twitter_block_bot.py` and insert the tweet URL (click on "Copy link to tweet" in the tweet menu), and the number of accounts to block,
- or run and configure `Notebook-Twitter Block Bot.ipynb` to your liking
#### Note:
Twitter only loads a couple of accounts at one time, so you can input a large number of accounts to block, but the bot will finish much before as Twitter delays loading more accounts by some minutes.
