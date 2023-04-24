# requests
import requests
import urllib
import urllib.request
from urllib.request import urlopen
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from urllib.request import urlopen, Request

# data, strucuture and maths
import pandas as pd
import numpy as np
import math
import json
import string
from more_itertools import unique_everseen
import random

# progress,performance and management
from tqdm.notebook import tqdm
import threading
import os
import ssl
from IPython.display import clear_output
import platform
import os

# imports used in Selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

# time
from time import sleep
import time

# text processing / regex
import regex
import re

# make wide
from IPython.display import display, HTML

display(HTML("<style>.container { width:100% !important; }</style>"))

# passwords
import getpass
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('credentials.ini')


class InstagramScraper():
    """
    Class that allows you to scrape the content of Instagram posts, either
    a profile or a hashtag.

    Initialised with the location of your Chromedriver location

    """

    def __init__(self, driver_loc=CONFIG['DEFAULT']['chromedriver_path']):

        self.driver_loc = driver_loc

    def userDetails(self):

        """
        Functions that capture log in details and logs user into Instagram

        Args:

            None needed

        Returns:

            Nothing

        """
        # username = input('Enter username...')
        # password = getpass.getpass(prompt='Enter password...')
        username = CONFIG['DEFAULT']['username']
        password = CONFIG['DEFAULT']['password']

        self._password = password  # retain password as attribute
        self._username = username  # retain user name as attribute

        return

    def openWebdriver(self):

        """
        Launches Chrome webdriver

        Args:

            None needed

        Returns:

            driver

        """

        # intiate driver
        print("Launching driver...")

        # retain current driver as attribute
        driver = webdriver.Chrome(self.driver_loc)

        return driver

    def closeWebdriver(self, driver):

        """
        Closes Chrome webdriver

        Args:

            webDriver

        Returns:

            Nothing

        """

        driver.close()

        return

    def instagramLogin(self, driver):

        """
        Logs in to Instagram

        Args:

            Current webdriver

        Returns:

            Current webdriver - logged into Instagram

        """

        # base url
        driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

        sleep(5)  # wait

        username = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        # enter username and password
        username.clear()
        username.send_keys(self._username)
        password.clear()
        password.send_keys(self._password)

        # target the login button and click it
        button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        '''
        time.sleep(5)
        alert = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Nie teraz")]'))).click()
        alert2 = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Nie teraz")]'))).click()
        '''
        return driver

    def setTarget(self):

        """
        Function that sets either a profile or a hashtag as a target

        Args:

            None

        Returns:

            base url to scrape - either a hashtag page or a profile page

        """

        # tou can choose either hashtag search or a profile to search
        route = input('What do you want to scrape, profile posts or hashtags? (p/h)')

        # if hashtags
        if route == 'h':

            # set hashtag
            hashtag = input('Which hashtag do you want to scrape posts for: ')

            self.target_label = '#' + hashtag  # retain hashtag as attribute

            tag_url = 'https://www.instagram.com/explore/tags/'  # set base url

            self._target = tag_url + hashtag  # set url to scrape from

            return self._target  # return url to scrape from

        else:

            profile = input('What profile do you want to scrape posts for: ')

            self.target_label = '@' + profile  # retain profile as attribute

            profile_url = 'https://www.instagram.com/'  # set base url

            self._target = profile_url + profile  # set url to scrape from

            return self._target  # return url to scrape from

    def scrapeLinks(self, url):

        """
        Function that scrapes the links needed

        Args:

            target_url

        Returns:

            Nothing - but retains a list of urls to scrape

        """

        # pass url as argument to Selenium webDriver, loads url
        self.activedriver.get(url)

        options = webdriver.ChromeOptions()

        # start maximised
        options.add_argument("--start-maximized")

        # gets scroll height
        last_height = self.activedriver.execute_script("return document.body.scrollHeight")

        # initiate empty list for unique Instagram links
        links = []

        # some lines for user interactivity / selection of link target(n)
        print("\n")
        target = input("How many links do you want to scrape (minimum)?: ")
        print("\n")
        print("Staring Selenium scrape, please keep browser open.")
        print("\n")

        # this loops round until n links achieved or page has ended

        while True:

            source = self.activedriver.page_source

            data = BeautifulSoup(source, 'html.parser')

            body = data.find('body')

            # script = body.find('span')

            for link in body.findAll('a'):

                if re.match("/p", link.get('href')):

                    links.append('https://www.instagram.com' + link.get('href'))

                else:
                    continue

            # Scroll down to bottom
            self.activedriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(10)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.activedriver.execute_script("return document.body.scrollHeight")

            # if no more content, scrape loop is terminated
            if new_height == last_height:
                break

            last_height = new_height

            # update on successful links scraped
            print("Scraped ", len(links), " links, ", len(set(links)), ' are unique')

            # if n target met then while loop breaks
            if len(set(links)) > int(target):
                break

        # links are saved as an attribute for the class instance
        self._links = list(unique_everseen(links))
        # clear the screen and provide user feedback on performance
        clear_output()

        print(links)
        # print(data)
        print("Finished scraping links. Maxed out at ", len(links), " links, of which ", len(self._links),
              ' are unique.')

        print("\n")

        print("Unique links obtained. Closing driver")

        print("\n")
        # close driver
        self.closeWebdriver(self.activedriver)

        return self._links

    # get user details, log in and initiate driver
    def logIn(self):

        self.userDetails()

        driver = self.openWebdriver()

        self.activedriver = self.instagramLogin(driver)

        clear_output()

        print('Successfully logged in..ready to scrape')

    # get all the unique links
    def getLinks(self):

        return self.scrapeLinks(self.setTarget())

    def DataFrame(self, links):
        post_username = []
        post_desc = []
        post_likes = []
        post_comments = []
        post_location = []
        post_url = []

        for link in links:
            page = urlopen(link).read()  # read url
            post_url.append(link)

            data = BeautifulSoup(page, 'html.parser')  # get a BeautifulSoup object

            script_tag = data.find('script', {'type': 'application/ld+json'})
            if script_tag:
                json_str = script_tag.string
                try:
                    json_obj = json.loads(json_str)
                    #print(json_obj)
                except ValueError as e:
                    print("Nie udało się przekształcić HTML na JSON:", e)
            else:
                print("Nie znaleziono tagu <script> z danymi JSON.")

            author_username = json_obj['author']['identifier']['value']
            post_username.append(author_username)

            post = json_obj['articleBody']
            post_desc.append(post)

            if json_obj['contentLocation'] == None:
                post_location.append("None")
            else:
                location = json_obj['contentLocation']['name']
                post_location.append(location)

            if 'interactionStatistic' in json_obj:
                interaction_statistic = json_obj['interactionStatistic']
                for interaction in interaction_statistic:
                    if 'interactionType' in interaction and interaction[
                        'interactionType'] == 'http://schema.org/LikeAction':
                        likes = interaction['userInteractionCount']
                        post_likes.append(likes)
                    else:
                        comments = interaction['userInteractionCount']
                        post_comments.append(comments)

        data = {
            'Link': post_url,
            'Username': post_username,
            'Description': post_desc,
            'Likes': post_likes,
            'Comments': post_comments,
            'Location': post_location
        }

        df = pd.DataFrame(data)

        return df


togetherness = InstagramScraper()
togetherness.logIn()
#togetherness.getLinks()

links = togetherness.getLinks()
df = togetherness.DataFrame(links)

display(df)


