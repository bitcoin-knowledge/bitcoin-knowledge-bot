import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located

class Webscrape:
    def __init__(self, additional_urls: list = [], blacklisted_urls: list = []):
        self.additional_urls = additional_urls
        self.blacklisted_urls = [*blacklisted_urls, "A Private Collector’s Guide to Art Collecting", "An introduction to /r/privatestudyrooms", 
        'Step-by-step: Documenting Anthony Gunin’s creation of The Most Holy Theotokos “Glykophilousa” icon', "Legacy",
        "Thoughts on Art Collecting", "Christ Pantocrator mosaic by Yury Yarin", "AH & Deater"]
        self.default_urls = {
            'mastering_bitcoin':['https://github.com/bitcoinbook/bitcoinbook/blob/develop/book.asciidoc'],
            'nakamoto_institute':['https://nakamotoinstitute.org/literature/', 'https://nakamotoinstitute.org/research/','https://nakamotoinstitute.org/mempool/'], 
            'chow_collection': ['https://chowcollection.medium.com'],
        }

    def get_urls(self):
        urls = self.default_urls + self.additional_urls
        for url in urls:
            if url in self.blacklisted_urls:
                continue
            yield url

    def mastering_bitcoin_sraper(self):
        articles = []
        parent_articles = []
        with webdriver.Firefox() as driver:
            driver.get(self.default_urls['mastering_bitcoin'][0])
            parent_pages = driver.find_elements_by_xpath("//a[@href]")
            for article in parent_pages:
                # ensure the link is an asciidoc and filter out appendex pages
                if ".asciidoc" in article.text and "appdx" not in article.text:
                    parent_articles.append(article.get_attribute("href"))

            for article in parent_articles:
                driver.get(article)
                articles.append({'title': driver.find_element_by_xpath("//h2").text, 'url': article})

        return articles

    def chow_collection_sraper(self):
        article_links = []
        with webdriver.Firefox() as driver:
            wait = WebDriverWait(driver, 10)
            driver.get(self.default_urls['chow_collection'][0])
            # Wait for show more button
            try:
                while driver.find_element_by_xpath("// button[contains(text(),'Show more')]"):
                    driver.find_element_by_xpath("// button[contains(text(),'Show more')]").click()
                    time.sleep(10)
            except:
                wait.until(presence_of_all_elements_located((By.XPATH, "//a[@class='eh bw']")))
                articles = driver.find_elements_by_xpath("//a[@class='eh bw']")
                for article in articles:
                    driver.get(article.get_attribute("href"))
                    article_links.append({'title': driver.find_element_by_xpath("//h1").text, 'url': article.get_attribute("href")})

        return article_links