# Modified for Image Alternates

import requests
import pprint
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def sort():
    df = pd.read_csv("image_alts.csv")
    sorted_list = []
    for i, element in df.iterrows():
        sorted_list.append([element["ratio"], element["present"], element["total"], element["website"]])
    sorted_list.sort()
    lsa_dict = {
        'website': [],
        "present": [],
        "total": [],
        "ratio": []
    }
    for element in sorted_list:
        lsa_dict["ratio"].append(element[0])
        lsa_dict["present"].append(element[1])
        lsa_dict["total"].append(element[2])
        split_website = element[3].split("/")
        if split_website[-1] != "":
            lsa_dict["website"].append(split_website[-1])
        else:
            lsa_dict["website"].append(split_website[-2])

    df = pd.DataFrame(lsa_dict)
    df.to_csv("image_alts_sorted.csv")


def generate_graphs():
    df = pd.read_csv("image_alts_sorted.csv")

    plt.hist(df["ratio"], bins=10)
    plt.xlabel("ratio")
    plt.ylabel("frequency")
    plt.title('Ratio distribution for LSA major websites')
    plt.legend()
    plt.show()
    plt.savefig('lsa_img_distribution.png')

    website_name = []
    '''
    website_list = df["website"][:10].append(df["website"][-10:])
    score_list = df["score"][:10].append(df["score"][-10:])
    plt.bar(website_list, score_list)
    '''
    plt.bar(df["website"][:10], df["ratio"][:10], color = 'b')
    plt.bar(df["website"][-10:], df["ratio"][-10:], color='g')
    plt.xlabel("website")
    plt.ylabel("score")
    plt.title('Ten Lowest and Highest Ratios for LSA major websites')
    plt.xticks(fontsize=9, rotation='vertical')
    plt.subplots_adjust(bottom=0.4)
    plt.savefig('lsa_img_score.png')
    plt.legend()
    plt.show()


def scrape_sites():
    websites = pd.read_csv("lsa.csv")
    lsa_websites = []
    lsa_dict = {
        'website': [],
        "present": [],
        "total": [],
        "ratio": []
    }
    for website in websites["LSA Sites"]:
        lsa_websites.append(website)
        URL = "https://www.digitalsales.com/alt-tag-checker"
        options = Options()
        options.headless = True
        driver = Chrome(options=options)
        driver.get(URL)
        web_addr = driver.find_element_by_id("inputname")
        web_addr.clear()
        driver.execute_script(f"document.getElementById('inputname').value='{website}';")
        submit = driver.find_element_by_name("single")
        submit.click()
        sleep(10)
        total_img = driver.find_element_by_id("totalimage")
        missing_alt = 0
        try:
            missing_alt = driver.find_element_by_id("missingalt")
            missing_alt = int(missing_alt.text)
        except NoSuchElementException:
            missing_alt = 0

        total_img = int(total_img.text)
        lsa_dict["website"].append(website)

        if total_img != 0:
            lsa_dict["present"].append(total_img - missing_alt)
            lsa_dict["total"].append(total_img)
            lsa_dict["ratio"].append((total_img - missing_alt) / total_img)
        else:
            lsa_dict["present"].append(0)
            lsa_dict["total"].append(0)
            lsa_dict["ratio"].append(1.0)

        print(website)

        if total_img != 0:
            print("present:", total_img - missing_alt)
            print("total:", total_img)
            print("ratio:", (total_img - missing_alt) / total_img)
        else:
            print("present: 0")
            print("total: 0")
            print("ratio: 1.0")

        print()
        driver.close()

    df = pd.DataFrame(lsa_dict)
    df.to_csv("image_alts.csv")
    ##button = driver.find_element_by_id("stats-type-notice")
    ##button.click()

def send_keys(el: WebElement, keys: str):
    for i in range(len(keys)):
        el.send_keys(keys[i])

if __name__ == '__main__':
    scrape_sites()
    sort()
    generate_graphs()
