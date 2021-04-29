from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import dotenv
import sys


class BlockBot(object):
    '''
    -----
    BlockBot class that handles logging into the user's account,
    loading tweets, and blocking the accounts that liked these
    tweets in question.
    -----
        Attributes:
            PATH (str): The path to the Chrome webdriver executable
                        file.
            num_accs (int): The maximum number of accounts to block
                            in each processed tweet.
            blocked_accounts (int): The total number of accounts that
                                    the bot has blocked.
            driver (WebDriver): The webdriver used in the object to
                                interact with webpages.
        -----
        Methods:
            __init__(PATH, num_accs): Initializes the BlockBot object
            close(): Terminate the webdriver and the BlockBot object
            login(): Login to the user's Twitter account
            format_tweet(tweet): Formats a tweet for webdriver use
            find_element_safe(element_type, element_attribute): Safely
                    find a WebElement in case the webpage takes too
                    long to load
            return_home(): Go to Twitter homepage
            block_users(tweets): Gets the list of tweets to block users
                    within, and steps through each tweet to block them.
            load_and_block_on_tweet(tweet, num_accs): Loads a tweet and
                    blocks all the users that liked it
    '''

    def __init__(self, PATH, num_accs):
        '''
        -----
        Initialize the object of type BlockBot.
        -----
            Parameters:
                PATH (str): The path to the Chrome webdriver
                            executable file.
                num_accs (int): The maximum number of accounts
                                to block in each processed tweet.
            -----
            Returns:
                None
        '''
        dotenv.load_dotenv()
        self.PATH = PATH
        self.driver = webdriver.Chrome(PATH)
        self.num_accs = num_accs
        self.blocked_accounts = 0
        self.login()

    def close(self):
        '''
        -----
        Quits all operations of the webdriver. Used when the object
        is not in use anymore.
        -----
            Parameters:
                None
            -----
            Returns:
                None
        '''
        driver = self.driver
        driver.quit()

    def login(self):
        '''
        -----
        The webdriver logs into the Twitter account.
        -----
            Parameters:
                None
            -----
            Returns:
                None
        '''
        # load random tweet and login
        driver = self.driver
        tweet = self.format_tweet('https://twitter.com/Oreo/status/1365038991469281280?s=20')
        driver.get(tweet)
        btn_login = self.find_element_safe("LINK_TEXT", "Log in")
        btn_login.click()

        # input user details
        user_input = self.find_element_safe('XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        user_input.send_keys(os.environ['USER_NAME'])
        pass_input = self.find_element_safe('XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        pass_input.send_keys(os.environ['PASS'])

        # move to login button and click
        mouse_move_login_btn = ActionChains(driver)
        btn_login = self.find_element_safe('XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
        mouse_move_login_btn.move_to_element(btn_login)
        mouse_move_login_btn.click()
        mouse_move_login_btn.perform()

        driver.implicitly_wait(5)

        # format apostrophe of possession for the account name
        user_name = os.environ['USER_NAME']
        poss = "'"
        if user_name[-1].lower() != 's':
            poss += 's'
        print(f"\nLogged into {user_name}{poss} account\n")

    def sleep_prevent_ratelimit(self, num_blocked, limit, seconds):
        '''
        -----
        A method to prevent rate-limiting by Twitter. It triggers
        a sleep if the number of blocked accounts has reached the
        limit, so this method can be called on each iteration of
        a loop.
        -----
            Parameters:
                num_blocked (int): The number of accounts currently
                                   blocked.
                limit (int): The number of accounts blocked that
                             will trigger a sleep.
                seconds (int): The number of seconds to sleep
            -----
            Returns:
                None
        '''
        if num_blocked % limit == 0:
            print(f"Sleeping for {seconds} seconds to prevent being rate-limited...")
            for sec in range(seconds):
                print(str(sec), end="..")
                sys.stdout.flush()
                time.sleep(1)
            
            print("")

    def format_tweet(self, tweet):
        '''
        -----
        When the button 'Click to share' on a tweet is clicked,
        the link received has extra useless information at the
        end of it which may cause bugs. So this method removes
        this extra information.
        -----
            Parameters:
                tweet (str): A tweet link either with or without
                             the extra information. The method
                             handles both types.
            -----
            Returns:
                (str): The tweet without the extra information
        '''
        return tweet.split("?")[0]

    def find_element_safe(self, element_type, element_attribute):
        '''
        -----
        Sometimes an element must be found before the webpage
        finishes loading. In those cases, this method allows
        the element to be found not immediately. As in, there
        is a delay so that the element can be found after the
        webpage fully loads and the element now exists.
        -----
            Parameters:
                element_type (str): The type of element that
                                    selenium uses for finding
                                    web elements -> 'XPATH',
                                    'ID', 'CLASS_NAME' etc.
                element_attribute (str): The attribute that the
                                         webdriver must search for
                                         -> 'div[class=...' etc.
            -----
            Returns:
                element (WebElement): The desired element if it is
                                      found within the time limit
                element (None): If the element is not found in time
        '''
        driver = self.driver

        if element_type == "CLASS_NAME":
            by_type = By.CLASS_NAME
        elif element_type == "CSS_SELECTOR":
            by_type = By.CSS_SELECTOR
        elif element_type == "ID":
            by_type = By.ID
        elif element_type == "LINK_TEXT":
            by_type = By.LINK_TEXT
        elif element_type == "NAME":
            by_type = By.NAME
        elif element_type == "PARTIAL_LINK_TEXT":
            by_type = By.PARTIAL_LINK_TEXT
        elif element_type == "TAG_NAME":
            by_type = By.TAG_NAME
        elif element_type == "XPATH":
            by_type = By.XPATH
        else:
            return None
            
        try:
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (by_type, element_attribute))
            )
        except:
            return None
        
        return element

    def return_home(self):
        '''
        -----
        Sometimes the account gets logged out on the current page,
        but this can be fixed by just going back to the home screen.
        This is all that this method does.
        -----
            Parameters:
                None
            -----
            Returns:
                None
        '''
        driver = self.driver
        driver.get("https://twitter.com/home")
        driver.implicitly_wait(5)
        time.sleep(1)
        driver.refresh()

    def block_users(self, tweets):
        '''
        -----
        Uses the list of tweets to step through each of them and
        block everyone that liked then. Shows detailed console
        messages for different cases.
        -----
            Parameters:
                tweets list(str): List of tweet links
            -----
            Returns:
                None
        '''
        total_blocked = 0
        for tweet in tweets:
            tweet = self.format_tweet(tweet)
            blocking = self.load_and_block_on_tweet(tweet, self.num_accs)
            if blocking is None:
                print(f"No accounts could be blocked on tweet: {tweet}\n")
            else:
                accs_format = "account"
                verb = "was"
                if blocking != 1:
                    accs_format += "s"
                    verb = "were"
                    
                print(f"{blocking} {accs_format} {verb} blocked on tweet: {tweet}\n")
                total_blocked += blocking
                self.blocked_accounts += blocking

                # sleep to prevent being rate-limited
                if blocking > 70:
                    self.sleep_prevent_ratelimit(1, 1, 60)
                elif blocking > 40:
                    self.sleep_prevent_ratelimit(1, 1, round(blocking - 10))

                if total_blocked > 150 and blocking > 15:
                    self.sleep_prevent_ratelimit(1, 1, round(60 + total_blocked/4))
        
        users_format = "user was"
        if total_blocked != 1:
            users_format = "users were"

        print(f"{total_blocked} {users_format} blocked in total for the {len(tweets)} tweets given.")

    def load_and_block_on_tweet(self, tweet, num_accs):
        '''
        -----
        This is the method that uses the webdriver to click
        buttons and block users.
        -----
            Parameters:
                tweet (str): Link to the tweet
                num_accs (int): Maximum number of accounts to block
            -----
            Returns:
                num_blocked (int): Total number of accounts blocked
            -----
            Exceptions Raised:
                AssertionError: If no one has liked the tweet. 
                                Returns: 0
                IndexError: If there are no more accounts loaded by
                            Twitter. Returns: num_blocked (int)
        '''
        driver = self.driver
        driver.get(tweet)

        # while on tweet
        time.sleep(2.5)
        a_likes = None
        links = driver.find_elements_by_xpath('.//a') # get all anchor tags
        for link in links:
            # Find the anchor tag that goes to the list of accounts that liked
            # the tweet in question:
            if link.get_attribute('href').split("/")[-1].lower() == "likes":
                a_likes = link
                break
        
        # make sure there is a link to likes (at least one user has liked the tweet)
        try:
            assert a_likes is not None
        except AssertionError:
            print("No one has liked this tweet.")
            self.return_home()
            return 0
        except:
            print("Some strange error ocurred.")
            self.return_home()
            return 0

        a_likes.click()
        driver.implicitly_wait(2)

        num_blocked = 0

        try:
            for _ in range(num_accs):
                # get the accounts that show up on screen then click the first account
                accounts = driver.find_elements_by_css_selector("div[class='css-18t94o4 css-1dbjc4n r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg']")
                block_account_action = ActionChains(driver)
                block_account_action.move_to_element_with_offset(accounts[0], 0, 20)
                block_account_action.click()
                block_account_action.perform()
                driver.implicitly_wait(2)

                # click the triple dots for account options
                btn_dots = self.find_element_safe('XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]')
                block_account_action = ActionChains(driver)
                block_account_action.move_to_element(btn_dots)
                block_account_action.click()
                block_account_action.perform()
                driver.implicitly_wait(2)
                time.sleep(0.5)

                # click the block button
                btn_block = self.find_element_safe('XPATH', '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[4]')
                block_account_action = ActionChains(driver)
                block_account_action.move_to_element(btn_block)
                block_account_action.click()
                block_account_action.perform()

                # click to confirm block
                btn_block_confirm = self.find_element_safe('XPATH', '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[3]/div[2]')
                block_account_action = ActionChains(driver)
                block_account_action.move_to_element(btn_block_confirm)
                block_account_action.click()
                block_account_action.perform()

                # go back to accounts list page and refresh
                num_blocked += 1
                driver.back()
                time.sleep(0.5)
                driver.refresh()
                time.sleep(1)

                out = " account"
                if num_blocked != 1:
                    out += "s"
                print("Blocked ", num_blocked, out)

                # sleep 60 secs to prevent being rate-limited
                sleep_secs = 60
                if num_blocked > 100:
                    sleep_secs += 60
                if num_blocked > 150:
                    sleep_secs += round(num_blocked/2)

                self.sleep_prevent_ratelimit(num_blocked, 25, sleep_secs)
        
        except IndexError:
            print("No more accounts loaded by Twitter for this tweet. Wait some time and try again.")
        
        except:
            print("Some uncaught error ocurred.")

        finally:
            if num_blocked == 0:
                self.return_home()
            return num_blocked


if __name__ == "__main__":
    PATH = "C:/Program Files (x86)/chromedriver_win32/chromedriver.exe"
    tweet_links = []

    text_path = "tweets.txt"
    if os.path.isdir("Scripts & Notebooks"):
        text_path = "Scripts & Notebooks/" + text_path

    with open(text_path, "r") as f:
        for line in f:
            if line[:-1] != "" and line.replace(" ", "").replace("\t", "")[0] != "#":
                tweet_links.append(line[:-1])
    # print(tweet_links)
    num_accs = 1000

    tic = time.perf_counter()
    block_bot = BlockBot(PATH, num_accs)
    block_bot.block_users(tweet_links)
    block_bot.close()
    toc = time.perf_counter()
    print(f"\n\nTime taken to block {block_bot.blocked_accounts} accounts was {int((toc-tic)//60)} min {(toc-tic) - (toc-tic)//60*60:0.4f} s, with a rate of {block_bot.blocked_accounts/(toc-tic):0.4f} blocks/s")
