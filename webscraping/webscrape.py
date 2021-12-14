from selenium import webdriver

class Webscrape:
    def __init__(self, additional_urls: list = [], blacklisted_urls: list = []):
        self.additional_urls = additional_urls
        self.blacklisted_urls = blacklisted_urls
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