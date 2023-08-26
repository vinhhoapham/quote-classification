import scrapy
from os.path import basename
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://www.goodreads.com/quotes"]

    def get_category_name(self, url):
        """
        Get the category name from the url
        :param url: the url of the category
        :return: the category name
        """
        parsed = urlparse(url)
        category_name = basename(parsed.path)
        return category_name

    def extract_quote_from_html(self, html):
        html_soup = BeautifulSoup(html, 'html.parser')
        quoteText = html_soup.find("div", {"class": "quoteText"})
        quote = quoteText.get_text(strip=True, separator="\n").split("\n―")[0]

        return quote


    def sanitize(self, quote):
        """
        Sanitize the quote by removing all " and " characters, the new line character, and the "―" character
        :param quote:
        :return:  the sanitized quote
        """
        quote = quote.replace("\n", " ")
        quote = quote.replace("―", " ")
        quote = quote.replace("  ", "")
        quote = quote.replace("...", " ")
        quote = quote.strip()
        return quote

    def parse(self, response):
        xpath_to_category = '/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div/ul/li/a//@href'
        categories = response.xpath(xpath_to_category).getall()

        for category in categories:
            link_to_website = "https://www.goodreads.com"
            link_to_category = link_to_website + category
            yield scrapy.Request(link_to_category, callback=self.parse_quotes_from_category)

    def parse_quotes_from_category(self, response):

        # Write the category name to a file

        link = response.url

        print(link)

        category = self.get_category_name(link)

        # Save the category name to a file in the folder ../../Data/Qoutes
        filename = f"{category}.txt"

        # Write the quotes to a file
        quotes_content = response.css('.quoteText').extract()
        with open(filename, "a") as f:
            for content in quotes_content:
                quote = self.extract_quote_from_html(content)
                quote = self.sanitize(quote)
                if quote != "":
                    f.write(f"{quote}\n")

        tag_to_next_page = 'a.next_page::attr(href)'
        path_to_next_page = response.css(tag_to_next_page).extract_first()

        if path_to_next_page is not None:
            link_to_website = "https://www.goodreads.com"
            link_to_next_page = link_to_website + path_to_next_page
            yield scrapy.Request(link_to_next_page, callback=self.parse_quotes_from_category)
