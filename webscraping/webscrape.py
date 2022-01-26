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
            'bitcoin_resources': ['https://bitcoin-resources.com/articles/'],
            'bitcoiner_guide': [
                "https://bitcoiner.guide/wallet/", 
                "https://github.com/BitcoinQnA/BitcoinPrivacyGuide/blob/master/index.md", 
                "https://bitcoiner.guide/qna/"
            ],
        }

    def generate_data(self):
        urls = self.get_article_urls()
        formated_article_data = []
        formated_podcast_data = []
        # initate the webdriver
        with webdriver.Firefox() as driver:
            for article in urls['articles']:
                try:
                    driver.get(article['url'])
                    # Wait for the article to load
                    time.sleep(3)
                    body = driver.find_element_by_xpath("/html/body").text.split('\n')
                    for section in body:
                        cleaned_text = self.clean_text(section)
                        if cleaned_text == False:
                            pass
                        else:
                            formated_article_data.append({'title': article['title'], 'url': article['url'], 'body': cleaned_text, 'image': article['image']})
                except Exception as e:
                    print("Error loading article: " + article['title'])
                    print()
                    print(e)
                    print("----------------------------------------------------------------------------------------------------")

            for article in urls['podcasts']:
                try:
                    driver.get(article['url'])
                    # Wait for the article to load
                    time.sleep(3)
                    body = driver.find_element_by_xpath("/html/body").text.split('\n')
                    for section in body:
                        cleaned_text = self.clean_text(section)
                        if cleaned_text == False:
                            pass
                        else:
                            formated_podcast_data.append({'title': article['title'], 'url': article['url'], 'body': cleaned_text, 'image': article['image']})
                except Exception as e:
                    print("Error loading article: " + article['title'])
                    print()
                    print(e)
                    print("----------------------------------------------------------------------------------------------------")

        with open('./datasets/knowledge_datasets/bitcoin_articles.json', 'w') as outfile:
            for article in formated_article_data:
                json.dump(article, outfile)
                outfile.write('\n')

        with open('./datasets/knowledge_datasets/bitcoin_podcasts.json', 'w') as outfile:
            for article in formated_podcast_data:
                json.dump(article, outfile)
                outfile.write('\n')

    def get_article_urls(self):
        urls = {
            "articles": [],
            "podcasts": [],
        }
        chow_collection_urls = self.chow_collection_scraper()
        nakamoto_urls = self.nakamoto_institute_scraper()
        mastering_bitcoin_urls = self.mastering_bitcoin_scraper()
        bitcoin_resources_urls = self.bitcoin_resources_scraper()
        bitcoiner_guide_urls = self.bitcoiner_guide_scraper()
        urls['articles'] = bitcoin_resources_urls + bitcoiner_guide_urls + mastering_bitcoin_urls + nakamoto_urls
        urls['podcasts'] = chow_collection_urls
        return urls

    def clean_text(self, text):
        # Remove newlines
        text = text.replace('\n', ' ')
        # Find any string with more than one white space in between characters and replace with a single space
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
            driver.close()

        return articles

    def chow_collection_scraper(self):
        articles = []
        with webdriver.Firefox() as driver:
            wait = WebDriverWait(driver, 10)
            driver.get(self.parent_urls['chow_collection'][0])
            # Wait for page to load
            time.sleep(3)
            try:
                # Wait for show more button and click until its gone
                while driver.find_element_by_xpath("// button[contains(text(),'Show more')]"):
                    driver.find_element_by_xpath("// button[contains(text(),'Show more')]").click()
                    time.sleep(7)
            except:
                wait.until(presence_of_all_elements_located((By.XPATH, "//a[@class='eh bw']")))
                article_pages = driver.find_elements_by_xpath("//a[@class='eh bw']")
                for article in article_pages:
                    if article.text not in self.blacklisted_articles:
                        articles.append({"title": article.text, "url": article.get_attribute("href"), "image": None})
            driver.close()

        return articles

    def bitcoin_resources_scraper(self):
        articles = []
        blacklsited_urls = [
            "https://github.com/bitcoin-resources/bitcoin-resources.github.io/blob/master/CONTRIBUTING.md", "https://twitter.com/BtcResources",
            "https://github.com/bitcoin-resources/bitcoin-resources.github.io",
            "https://dergigi.com/support",
            "https://www.patreon.com/dergigi",
            "https://21lessons.com/",
            "https://www.bitcoin-quotes.com/",
            "https://opsecswag.com/",
            "https://dergigi.com/",
            "https://nakamotoinstitute.org/literature/",
            "https://anchor.fm/thecryptoconomy",
            "http://bitcoinrabbithole.org/writings/",
            "http://21lessons.com/"
            "https://www.bitcoin-quotes.com/",
        ]
        with webdriver.Firefox() as driver:
            driver.get(self.parent_urls['bitcoin_resources'][0])
            parent_pages = driver.find_elements_by_xpath("//a[@href]")
            for page in parent_pages:
                # ensure the link is an actual article and filter out blacklisted urls
                if not page.get_attribute("title") and "https://bitcoin-resources.com/" not in page.get_attribute("href") and page.get_attribute("href") not in blacklsited_urls:
                    articles.append({"title": page.text, "url": page.get_attribute("href"), "image": None})
            driver.close()

        return articles

    def bitcoiner_guide_scraper(self):
        articles = []
        bitcoin_wallet_guide = self.parent_urls['bitcoiner_guide'][0]
        bitcoin_privacy_guide = self.parent_urls['bitcoiner_guide'][1]
        bitcoin_qna = self.parent_urls['bitcoiner_guide'][2]
        for parent_page in self.parent_urls['bitcoiner_guide']:
            with webdriver.Firefox() as driver:
                if parent_page == bitcoin_wallet_guide:
                    driver.get(parent_page)
                    pages = driver.find_elements_by_xpath("//a[@href]")
                    for page in pages:
                        if "/wallet/" in page.get_attribute("href"):
                            articles.append({"title": "Bitcoin Wallet Guide " + page.text, "url": page.get_attribute("href"), "image": None})
                elif parent_page == bitcoin_privacy_guide:
                    driver.get(parent_page)
                    pages = driver.find_elements_by_xpath("//a[@href]")
                    for page in pages:
                        if '.md' in page.get_attribute("href") and '/index' not in page.get_attribute("href") and '/login' not in page.get_attribute("href"):
                            clean_endpoint = page.get_attribute("href").split("/")[-1]
                            correct_endpoint = clean_endpoint.replace(".md", "")
                            articles.append({"title": "Bitcoin Privacy Guide " + page.text, "url": "https://bitcoiner.guide/privacy/" + correct_endpoint, "image": None})
                elif parent_page == bitcoin_qna:
                    blacklisted_pages = ['Graphics', 'Recommendations', 'Education']
                    driver.get(parent_page)
                    pages = driver.find_elements_by_xpath("//a[@href]")
                    for page in pages:
                        parent_elem = page.find_element_by_xpath('..')
                        if '/qna/' in page.get_attribute("href") and page.text not in blacklisted_pages and parent_elem.tag_name == 'td':
                            articles.append({"title": "Bitcoin QnA " + page.text, "url": page.get_attribute("href"), "image": None})
                driver.close()

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
                        if link.get_attribute('href') in blacklisted_pages or 'https://nakamotoinstitute.org/mempool/series/' == link.get_attribute('href'):
                            pass
                        elif 'https://nakamotoinstitute.org/mempool/' in link.get_attribute('href'):
                            pages.append(link.get_attribute('href'))
                else:
                    # Get all articles that are hosted as HTML pages
                    anchors = driver.find_elements_by_xpath("//a[@href]")
                    for link in anchors:
                        if link.text == "HTML":
                            pages.append(link.get_attribute('href'))
            driver.close()

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