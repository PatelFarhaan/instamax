import pdb
import time
import random

import memcache
import requests
from flask import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from project import db
from project.users.models import Counter

client = memcache.Client([('127.0.0.1', 11211)])

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-extentions')
        self.options.add_argument('--enable-popup-blocking')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=self.options)
        self.session_items = {}

        self.unsuccess_request = 0

    def closeBrowser(self):
        self.driver.close()

    def get_random_user_agent(self):
        user_agents=[
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.8) Gecko/20071008 Firefox/2.0.0.8",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.7) Gecko/20070914 Firefox/2.0.0.7",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/3.0.183.1 Safari/531.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/3.0.187.1 Safari/531.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.1 Safari/532.0",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/531.3 (KHTML, like Gecko) Chrome/3.0.193.2 Safari/531.3",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.17 Safari/532.0",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
            "Opera/9.22 (Windows NT 5.1; U; en)",
            "Opera/9.24 (Windows NT 5.1; U; en)",
            "Opera/9.23 (Windows NT 5.1; U; en)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.1)"
        ]
        return user_agents[random.randint(0, len(user_agents) - 1)]

    def login(self, is_only_login=True):
        try:
            driver = self.driver
            driver.get("https://www.instagram.com/")
            time.sleep(2)
            login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
            login_button.click()
            time.sleep(2)
            user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
            user_name_elem.clear()
            user_name_elem.send_keys(self.username)
            passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
            passworword_elem.clear()
            passworword_elem.send_keys(self.password)
            passworword_elem.send_keys(Keys.RETURN)
            time.sleep(2)
            try:
                # allow button      -> aOOlW  bIiDR , not now button    -> class aOOlW   HoLwm
                item = driver.find_element_by_xpath('/html/body/div[3]')
                div_attibute = item.get_attribute("role")
                if div_attibute == "presentation":
                    not_now_button = item.find_element_by_xpath("div/div/div[3]/button[2]")
                    not_now_button.click()
            except Exception as error_item:
                print("not asked for notification", error_item)
                # login activity class _0ZPOP kIKUG
            try:
                try:
                    time.sleep(2)
                    button_1 = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]')
                    button_1.click()
                except Exception as error_2:
                    btn_inside = driver.find_element_by_xpath('//a[@href="/explore/"]')
                    size_check = btn_inside.size
                    if isinstance(size_check, dict):
                        print("No error logged in Successfully")
                    else:
                        print("Login Error 2", str(error_2))
                        # pdb.set_trace()
                        button_2=driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]')
                        button_2.click()
            except Exception as error_1:
                tp = str(int(time.time()))
                driver.save_screenshot(tp+".png")
                print("Login Error 1", str(error_1))

            if is_only_login == True:
                button_3 = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/a')
                button_3.click()
            else:
                self.refresh_session_items()
                # self.session_items=session_items

            return True
        except Exception as error_0:
            print("Login Error 0", str(error_0))
            # pdb.set_trace()
            return False

    def login2(self):
        try:
            driver = self.driver
            driver.get("https://www.instagram.com/")
            time.sleep(2)
            login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
            login_button.click()
            time.sleep(1)
            user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
            user_name_elem.clear()
            user_name_elem.send_keys(self.username)
            passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
            passworword_elem.clear()
            passworword_elem.send_keys(self.password)
            passworword_elem.send_keys(Keys.RETURN)
            try:
                try:
                    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
                except:
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
            except:
                pass

            return True
        except:
            return False

    def check_logout(self):
        try:
            user_name_elem=self.driver.find_element_by_xpath("//input[@name='username']")
            self.login(False)
        except Exception as error_item:
            print("user not logout yet", error_item)



    def get_pending_request_details(self):
        # pdb.set_trace()
        print("Getting List of Pending Request")

        url="https://www.instagram.com/accounts/activity/"

        querystring={"__a": "1", "include_reel": "true"}
        csrf_token = self.session_items["csrftoken"]
        session_id = self.session_items["sessionid"]
        mid = self.session_items["mid"]
        ds = self.session_items["ds_user_id"]

        headers={
            'Host': "www.instagram.com",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate, br",
            'X-CSRFToken': csrf_token,
            'Content-Type': "application/x-www-form-urlencoded",
            'X-Requested-With': "XMLHttpRequest",
            'Connection': "keep-alive",
            "Content-Length": "0",
            "Cookie": "csrftoken={ct};  sessionid={sid}; rur=FRC; mid={mid}; ds_user_id={ds};".format(ct=csrf_token, sid=session_id, mid=mid, ds=ds),
            'Cache-Control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()

        edge_follow_requests=response["graphql"]["user"]["edge_follow_requests"]["edges"]
        list_of_item_to_process=[]
        for follow_request_item in edge_follow_requests:
            node=follow_request_item["node"]
            list_of_item_to_process += [{"id": node["id"], "username": node["username"]}]
        return list_of_item_to_process

    def start_accepting_request(self, follow_request_list):
        # pdb.set_trace()

        db.isolation_level=None
        countval=Counter.query.filter_by(insta_username=session['insta_username']).first()

        if countval is None:
            print("init to -> 0 === ", client.set(session['insta_username'], 0))
            newcounts=Counter(insta_username=session['insta_username'])
            db.session.add(newcounts)
            db.session.commit()
            countval = Counter.query.filter_by(insta_username=session['insta_username']).first()

        constant_sleep = 0.25
        for i, item in enumerate(follow_request_list):
            user_id = item["id"]
            resp = self.accept_request(user_id)
            wait_time = random.random() + constant_sleep  # random.randint(0, 2) +
            print(i+1, "\t wait_time", wait_time, "counts", countval.counts)
            time.sleep(wait_time)
            try:
                if resp == True:
                    countval.counts = countval.counts+1
                    db.session.commit()
                else:
                    self.refresh_session_items()
            except Exception as erro:
                print("Unable to modify counts in db", erro)
            session.modified=True
            if (i+1) % 20 == 0:
                print("refeshing session")
                self.refresh_session_items()
        return

    def refresh_session_items(self):
        self.driver.refresh()
        cookies_items = self.driver.get_cookies()
        for item in cookies_items:
            self.session_items[item["name"]] = item["value"]

    def accept_request(self, user_id):

        url = "https://www.instagram.com/web/friendships/{}/approve/".format(user_id)
        csrf_token = self.session_items["csrftoken"]
        session_id = self.session_items["sessionid"]
        instagram_username = session['insta_username']

        headers={
            'Host': "www.instagram.com",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
            'Accept': "*/*",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate, br",
            'X-CSRFToken': csrf_token,
            'Content-Type': "application/x-www-form-urlencoded",
            'X-Requested-With': "XMLHttpRequest",
            'Connection': "keep-alive",
            'Referer': "https://www.instagram.com/factbullet/",
            'Content-Length': "0",
            "Cookie": "csrftoken={ct};  sessionid={sid}; rur=FRC;".format(ct=csrf_token, sid=session_id),
            'Cache-Control': "no-cache",
        }

        response = requests.request("POST", url, headers=headers)
        if response.status_code ==200:
            resp_json = response.json()
            if resp_json["status"] == "ok":
                print("Increment counter ", client.incr(instagram_username))
            return True
        else:
            print("error ---------->  ", response.status_code, user_id)
            print("Counter init", client.incr("total_failed_requests"+instagram_username))
            self.unsuccess_request += 1
            self.driver.get_screenshot_as_file("{}.png".format(user_id))
            if response.text == "Please wait a few minutes before you try again.":
                overload_issue = random.randint(4, 10)
                time.sleep(overload_issue)
            with open("{}.text".format(user_id), "w") as ftr:
                ftr.write(response.text)
            return False

    def check_memchache(self):
        # print("set, item", client.set(session['insta_username'], 10))
        ctr=client.get(session['insta_username'])
        print("get item", ctr)

    def pending_request_count(self):

        driver = self.driver

        try:
            try:
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
            except Exception as error_2:
                print("Pending Request Error 2",str(error_2))
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
        except Exception as error_1:
            print("Pending Request Error 1",str(error_1))

        try:
            time.sleep(2)
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
            except Exception as try_error_2:
                print("Pending Request try Error 2", str(try_error_2))
                driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
        except Exception as try_error_1:
            print("Pending Request try Error 1", str(try_error_1))
        driver.find_element_by_xpath("/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[2]/a/span").click()
        time.sleep(2)

        try:
            try:
                pending_count = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "JRHhD")))
                pending_count_requests = int(pending_count.text)

                return pending_count_requests
            except:
                pending_count = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "JRHhD")))
                pending_count = pending_count.text[:-1]
                pending_count_requests = int(pending_count)

                return 1000
        except:
            return "No request to accept"


    # def accept_pending_requests(self, request_accept_count):
    #
    #     print('in pending requests')
    #     driver = self.driver
    #     var1 = int(request_accept_count/15)
    #     var2 = request_accept_count%15
    #     counter = 0
    #
    #     client.set(session['insta_username'], counter)
    #     db.isolation_level = None
    #     countval = Counter.query.filter_by(insta_username=session['insta_username']).first()
    #
    #     if countval is None:
    #         newcounts = Counter(insta_username=session['insta_username'])
    #         db.session.add(newcounts)
    #         db.session.commit()
    #         countval = Counter.query.filter_by(insta_username=session['insta_username']).first()
    #
    #     try:
    #         if var1 > 0:
    #             for j in range(0, var1):
    #                 try:
    #                     try:
    #                         driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
    #                     except:
    #                         driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
    #                 except:
    #                     pass
    #
    #                 try:
    #                     driver.find_element_by_xpath("/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[2]/a/span").click()
    #                 except:
    #                     pass
    #
    #                 WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "M_9ka"))).click()
    #
    #                 for i in range(1, 16):
    #
    #                     xpath_for_confirm = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div/div[4]/div/div[1]/div/div[{count}]/div[3]/div/div[1]/button'.format(count=i)
    #                     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_for_confirm))).click()
    #                     time.sleep(0.7)
    #                     counter+= 1
    #
    #                     client.incr(session['insta_username'])
    #
    #                     try:
    #                         countval.counts = counter
    #                         db.session.commit()
    #                     except:
    #                         i = i
    #                         time.sleep(0.05)
    #
    #                     session.modified = True
    #                     time.sleep(0.05)
    #                     print('set: ', counter)
    #
    #
    #                 time.sleep(4)
    #                 driver.find_element_by_xpath(
    #                     '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div').click()
    #
    #             return "{} Requests Accepted".format(request_accept_count)
    #
    #
    #         if not var2 == 0:
    #             try:
    #                 try:
    #                     driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
    #                 except:
    #                     driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
    #             except:
    #                 pass
    #             WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "M_9ka"))).click()
    #             try:
    #                 for i in range(1, var2+1):
    #                     xpath_for_confirm = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div/div[4]/div/div[1]/div/div[{count}]/div[3]/div/div[1]/button'.format(
    #                         count=i)
    #                     WebDriverWait(driver, 5).until(
    #                         EC.presence_of_element_located((By.XPATH, xpath_for_confirm))).click()
    #
    #                 return "{} Requests Accepted".format(request_accept_count)
    #
    #             except:
    #                 return "No request to accept"
    #     except:
    #         return "All requests Accepted"
