from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import dotenv

def twitter_block_bot(tweet_link, num_accs):
    def find_element_safe(driver, element_type, element_attribute):
        
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

    # inputs:
    tweet_link = tweet_link.split("?")[0]

    # tweet_link = input("Tweet link (Copy link to tweet): ")
    # tweet_link = tweet_link.split("?")[0]
    # num_accs = int(input("Number of accounts: "))

    # start bot
    PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    dotenv.load_dotenv()

    driver.get(tweet_link)
    btn_login = find_element_safe(driver, "LINK_TEXT", "Log in")
    btn_login.click()

    # input user details
    user_input = find_element_safe(driver, 'XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
    user_input.send_keys(os.environ['USER_NAME'])
    pass_input = find_element_safe(driver, 'XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
    pass_input.send_keys(os.environ['PASS'])

    # move to login button and click
    mouse_move_login_btn = ActionChains(driver)
    btn_login = find_element_safe(driver, 'XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
    mouse_move_login_btn.move_to_element(btn_login)
    mouse_move_login_btn.click()
    mouse_move_login_btn.perform()

    driver.implicitly_wait(5)

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

    assert a_likes is not None
    a_likes.click()
    driver.implicitly_wait(2)

    num_blocked = 0

    try:
        for _ in range(num_accs):
            accounts = driver.find_elements_by_css_selector("div[class='css-18t94o4 css-1dbjc4n r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg']")
            block_account_action = ActionChains(driver)
            block_account_action.move_to_element_with_offset(accounts[0], 0, 20)
            block_account_action.click()
            block_account_action.perform()
            driver.implicitly_wait(2)

            btn_dots = find_element_safe(driver, 'XPATH', '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]')
            block_account_action = ActionChains(driver)
            block_account_action.move_to_element(btn_dots)
            block_account_action.click()
            block_account_action.perform()
            driver.implicitly_wait(2)
            time.sleep(0.5)

            btn_block = find_element_safe(driver, 'XPATH', '//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div[4]')
            block_account_action = ActionChains(driver)
            block_account_action.move_to_element(btn_block)
            block_account_action.click()
            block_account_action.perform()

            btn_block_confirm = find_element_safe(driver, 'XPATH', '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[3]/div[2]')
            block_account_action = ActionChains(driver)
            block_account_action.move_to_element(btn_block_confirm)
            block_account_action.click()
            block_account_action.perform()

            num_blocked += 1
            driver.back()
            time.sleep(0.5)
            driver.refresh()
            time.sleep(1)

            out = " account"
            if num_blocked != 1:
                out += "s"
            print("Blocked ", num_blocked, out)
    
    except IndexError:
        print("No more accounts loaded by twitter. Wait some time and try again.")
    
    except:
        print("Some uncaught error ocurred.")

    finally:
        driver.quit()
        return num_blocked


if __name__ == "__main__":
    tweet_link = input("Tweet link (Copy link to tweet): ")
    num_accs = int(input("Number of accounts: "))
    num_blocked = twitter_block_bot(tweet_link, num_accs)
    print("\n\nBlocked ", num_blocked, " accounts in total")
