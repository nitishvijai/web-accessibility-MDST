import requests
import pprint
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def sort():
    df = pd.read_csv("output.csv")
    sorted_list = []
    for i, element in df.iterrows():
        sorted_list.append([element["score"], element["high"], element["medium"], element["low"], element["website"]])
    sorted_list.sort()
    lsa_dict = {
        'website': [],
        'low': [],
        "medium": [],
        "high": [],
        "score": []
    }
    for element in sorted_list:
        lsa_dict["score"].append(element[0])
        lsa_dict["high"].append(element[1])
        lsa_dict["medium"].append(element[2])
        lsa_dict["low"].append(element[3])
        split_website = element[4].split("/")
        if split_website[-1] != "":
            lsa_dict["website"].append(split_website[-1])
        else:
            lsa_dict["website"].append(split_website[-2])

    df = pd.DataFrame(lsa_dict)
    df.to_csv("output_sorted.csv")


def generate_graphs():
    df = pd.read_csv("output_sorted.csv")

    plt.hist(df["score"], bins=10)
    plt.xlabel("score")
    plt.ylabel("frequency")
    plt.title('Score distribution for LSA major websites')
    plt.legend()
    plt.show()
    plt.savefig('lsa_distribution.png')

    website_name = []
    '''
    website_list = df["website"][:10].append(df["website"][-10:])
    score_list = df["score"][:10].append(df["score"][-10:])
    plt.bar(website_list, score_list)
    '''
    plt.bar(df["website"][:10], df["score"][:10], color = 'b')
    plt.bar(df["website"][-10:], df["score"][-10:], color='g')
    plt.xlabel("website")
    plt.ylabel("score")
    plt.title('Ten Lowest and Highest Score for LSA major websites')
    plt.xticks(fontsize=9, rotation='vertical')
    plt.subplots_adjust(bottom=0.4)
    plt.savefig('lsa_score.png')
    plt.legend()
    plt.show()


def scrape_sites():
    websites = pd.read_csv("lsa.csv")
    lsa_websites = []
    lsa_dict = {
        'website': [],
        'low': [],
        "medium": [],
        "high": [],
        "score": []
    }
    for website in websites["LSA Sites"]:
        lsa_websites.append(website)
        URL = f"https://www.accessi.org/?{website}"
        options = Options()
        options.headless = True
        driver = Chrome(chrome_options=options)
        driver.get(URL)
        sleep(15)
        high_score = 0
        high = 0
        medium_score = 0
        medium = 0
        low_score = 0
        low = 0
        cats = driver.find_elements_by_class_name("test-result-block")
        for i in cats:
            if i.get_attribute("style") == "":
                header = i.find_element_by_class_name("test-result-header")
                num_impacts = header.find_element_by_class_name("test-result-count")
                num_impacts = str(num_impacts.text)
                if "high" in num_impacts:
                    number = num_impacts.split(" ")[0]
                    high += int(number)
                    high_score += 3 * int(number)
                elif "medium" in num_impacts:
                    number = num_impacts.split(" ")[0]
                    medium += int(number)
                    medium_score += 2 * int(number)
                elif "low" in num_impacts:
                    number = num_impacts.split(" ")[0]
                    low += int(number)
                    low_score += int(number)
        lsa_dict["website"].append(website)
        lsa_dict["low"].append(low)
        lsa_dict["medium"].append(medium)
        lsa_dict["high"].append(high)
        lsa_dict["score"].append(medium_score + high_score)
        print(website)
        print("low:", low)
        print("medium:", medium)
        print("high:", high)
        print("final score:", medium_score + high_score)
        print()
        driver.close()

    df = pd.DataFrame(lsa_dict)
    df.to_csv("output.csv")
    ##button = driver.find_element_by_id("stats-type-notice")
    ##button.click()


if __name__ == '__main__':
    scrape_sites()
    sort()
    generate_graphs()
