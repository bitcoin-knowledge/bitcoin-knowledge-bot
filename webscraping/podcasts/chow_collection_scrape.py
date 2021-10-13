import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located, element_to_be_clickable

article_links = []
data = []

def click_show_more():
    try:
        #logic to load the page. If it is successful, it will not go to except.
        driver.find_element_by_xpath("// button[contains(text(),'Show more')]").click()
        return False
    except:
        driver.find_element_by_xpath("// button[contains(text(),'Show more')]").click()
        return True

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://chowcollection.medium.com")
    # Wait for show more button
    try:
        while driver.find_element_by_xpath("// button[contains(text(),'Show more')]"):
            driver.find_element_by_xpath("// button[contains(text(),'Show more')]").click()
            time.sleep(10)
    except:
        articles = driver.find_elements_by_xpath("//a[@class='eh bw']")
        for article in articles:
            article_links.append(article.get_attribute("href"))

        for link in article_links:
                driver.get(link)
                # Waiting for footer to render which means all of the text has rendered
                wait.until(presence_of_all_elements_located((By.XPATH, "//p")))
                text = driver.find_elements_by_xpath("//p")
                title = driver.find_element_by_xpath("//h1")
                for section in text:
                    try:
                        j = {
                            "link": link,
                            "title": title.text,
                            "text": section.text
                        }
                        data.append(j)
                    except:
                        print("Error")

with open('./datasets/chow_collection_scrape.json', 'w') as outfile:    
    for obj in data:
        json.dump(obj, outfile)
        outfile.write('\n')