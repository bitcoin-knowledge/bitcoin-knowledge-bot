import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located

class Webscrape:
    def __init__(self, additional_urls: list = [], additional_blacklisted_articles: list = []):
        self.additional_urls = additional_urls
        self.blacklisted_articles = [*additional_blacklisted_articles, "A Private Collector’s Guide to Art Collecting", "An introduction to /r/privatestudyrooms", 
        'Step-by-step: Documenting Anthony Gunin’s creation of The Most Holy Theotokos “Glykophilousa” icon', "Legacy",
        "Thoughts on Art Collecting", "Christ Pantocrator mosaic by Yury Yarin", "AH & Deater"]
        self.parent_urls = {
            'mastering_bitcoin':['https://github.com/bitcoinbook/bitcoinbook/blob/develop/book.asciidoc'],
            'nakamoto_institute':['https://nakamotoinstitute.org/literature/', 'https://nakamotoinstitute.org/research/','https://nakamotoinstitute.org/mempool/'], 
            'chow_collection': ['https://chowcollection.medium.com'],
        }

    def generate_data(self):
        articles = self.get_articles()
        formated_data = []
        for article in articles:
            with webdriver.Firefox() as driver:
                wait = WebDriverWait(driver, 1)
                driver.get(article['url'])
                wait.until(presence_of_all_elements_located((By.XPATH, "//p")))
                try:
                    text_content = driver.find_elements_by_xpath("//p")
                    for section in text_content:
                        cleaned_text = self.clean_text(section.text)
                        if cleaned_text == False:
                            break
                        formated_data.append({'title': article['title'], 'url': article['url'], 'body': cleaned_text, 'image': article['image']})
                except:
                    print("Error loading article: " + article['title'])

        with open('./datasets/knowledge_datasets/bitcoin_knowledge.json', 'w') as outfile:
            for article in formated_data:
                json.dump(article, outfile)
                outfile.write('\n')

    def get_articles(self):
        nakamoto_urls = self.nakamoto_institute_scraper()
        mastering_bitcoin_urls = self.mastering_bitcoin_scraper()
        chow_collection_urls = self.chow_collection_scraper()
        urls = mastering_bitcoin_urls + chow_collection_urls + nakamoto_urls
        return urls

    def clean_text(self, text):
        # Remove newlines
        text = text.replace('\n', ' ')
        # Filter out any string with more than one white space in between characters
        re.sub(" +", ' ', text)
        # Remove all non ascii chars
        stripped_text = text.encode("ascii", "ignore")
        stripped_text = stripped_text.decode()
        # Filter out if it is not a string or it is empty
        if not str(text) or text == None:
            return False
        # Filter out any string with more whitespaces than chars
        num_of_letters = len(stripped_text) - stripped_text.count(" ")
        if stripped_text.count(" ") > num_of_letters:
            return False

        if len(stripped_text) <= 40:
            return False
        
        return stripped_text

    def mastering_bitcoin_scraper(self):
        articles = []
        parent_articles = []
        mastering_bitcoin_cover = 'https://github.com/bitcoinbook/bitcoinbook/blob/develop/images/cover.png?raw=true'
        with webdriver.Firefox() as driver:
            driver.get(self.parent_urls['mastering_bitcoin'][0])
            parent_pages = driver.find_elements_by_xpath("//a[@href]")
            for article in parent_pages:
                # ensure the link is an asciidoc and filter out appendex pages
                if ".asciidoc" in article.text and "appdx" not in article.text:
                    parent_articles.append(article.get_attribute("href"))

            for article in parent_articles:
                driver.get(article)
                chapter = driver.find_elements_by_xpath("//h2")
                articles.append({'title': "Mastering bitcoin - " + chapter[1].text, 'url': article, 'image': mastering_bitcoin_cover})
        return articles

    def chow_collection_scraper(self):
        article_links = []
        articles = []
        with webdriver.Firefox() as driver:
            wait = WebDriverWait(driver, 10)
            driver.get(self.parent_urls['chow_collection'][0])
            # Wait for show more button
            try:
                while driver.find_element_by_xpath("// button[contains(text(),'Show more')]"):
                    driver.find_element_by_xpath("// button[contains(text(),'Show more')]").click()
                    time.sleep(7)
            except:
                wait.until(presence_of_all_elements_located((By.XPATH, "//a[@class='eh bw']")))
                article_pages = driver.find_elements_by_xpath("//a[@class='eh bw']")
                for article in article_pages:
                    article_links.append(article.get_attribute("href"))

            for article in article_links:
                driver.get(article)
                # Want to grab the podcast images eventually if avilable
                image = None
                title = driver.find_element_by_xpath("//h1").text
                articles.append({'title': title, 'url': article, 'image': image})
            
        return articles

    def nakamoto_institute_scraper(self):
        articles = []
        pages = []
        # Speicifc nakamoto pages we need to ignore
        blacklisted_pages = ['https://nakamotoinstitute.org/mempool/authors', 'https://nakamotoinstitute.org/mempool/series', 'https://nakamotoinstitute.org/mempool/feed/', 
        'https://nakamotoinstitute.org/', 'https://satoshi.nakamotoinstitute.org/', 'https://nakamotoinstitute.org/mempool/']
        driver = webdriver.Firefox()
        with webdriver.Firefox() as driver:
            for knowledge_source in self.parent_urls['nakamoto_institute']:
                driver.get(knowledge_source)
                # Scrape is slightly different on mempool page
                if knowledge_source == 'https://nakamotoinstitute.org/mempool/':
                    anchors = driver.find_elements_by_xpath("//a[@href]")
                    for link in anchors:
                        # Avoid blacklisted urls and links to the series pages
                        if link.get_attribute('href') in blacklisted_pages or 'https://nakamotoinstitute.org/mempool/series/' in link.get_attribute('href'):
                            pass
                        elif 'https://nakamotoinstitute.org/mempool/' in link.get_attribute('href'):
                            pages.append(link.get_attribute('href'))
                else:
                    # Get all articles that are hosted as HTML pages
                    anchors = driver.find_elements_by_xpath("//a[@href]")
                    for link in anchors:
                        if link.text == "HTML":
                            pages.append(link.get_attribute('href'))

            for article in pages:
                with webdriver.Firefox() as driver:
                    driver.get(article)
                    title = driver.find_element_by_xpath("//h1").text
                    image = driver.find_element_by_xpath("//img").get_attribute("src") if driver.find_element_by_xpath("//img") else None
                    obj = {
                        'title': title,
                        'url': article,
                        'image': image,
                    }
                    articles.append(obj)
                    driver.close()
        return articles

test = Webscrape()
test.generate_data()