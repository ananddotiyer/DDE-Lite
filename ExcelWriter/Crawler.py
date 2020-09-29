#############################################################################################################################################
__filename__ = "Crawler.py"
__description__ = """Extracts web elements from html page.  Wrapped in functions.py

"""

__author__ = "Anand Iyer"
__copyright__ = "Copyright 2016-17, Anand Iyer"
__credits__ = ["Anand Iyer"]
__version__ = "2.6"
__maintainer__ = "Anand Iyer"
__email__ = "anand.iyer@moolya.com"
__status__ = "Testing" #Upgrade to Production once tested to function.
#############################################################################################################################################
import scrapy
from scrapy import selector
import functions
import support

domain = ""

current_module = __import__(__name__)

return_parse_links = []
return_parse_xpath = ""
return_parse_amazon_pages = ""

class HTMLSpider(scrapy.Spider):
    name = "articles"
    def __init__(self,url, xpath, parse_function):
        self.url = url
        self.parse_function = parse_function
        self.xpath = xpath

        global domain
        domain = url.split ("//")[1].split ('/')[0]

    def start_requests(self):
        self.parse = getattr (self, self.parse_function)
        
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse_links (self, response):
        link_list = []
        
        if self.xpath == "":
            self.xpath = article_identifier[domain]
            
        all_links = response.selector.xpath("//" + self.xpath + "/descendant::a")
        for each_link in all_links:
            href = support.extract_xpath (each_link, "attribute::href", True)
            desc = support.extract_xpath (each_link, "text()")
            if desc != "":
                link_list.append ('=HYPERLINK("' + href.encode('utf8') + '","' + desc.encode('utf8') + '")')
        
        global return_parse_links
        return_parse_links = link_list

    def parse_xpath (self, response):
        return_value = response.selector.xpath("//" + self.xpath).extract()
        
        global return_parse_xpath
        return_parse_xpath = return_value

    def parse_amazon_pages (self, response):
        item_list = []
        
        index = 0
        all_titles = response.selector.xpath("//li/descendant::a[@class='a-link-normal s-access-detail-page  a-text-normal']")
        for each_title in all_titles:
            title = support.extract_xpath (each_title, "attribute::title")
            href = support.extract_xpath (each_title, "attribute::href", True)
            item = '=HYPERLINK("' + href.encode('utf8') + '","' + title.encode('utf8') + '")'        
            item_list.append ({})
            item_list[index]["title"] = item
            index += 1

        index = 0
        all_makers = response.selector.xpath("//li/descendant::a[@class='a-link-normal s-access-detail-page  a-text-normal']/../../div[2]/span[2]")
        for each_maker in all_makers:
            maker = support.extract_xpath (each_maker, "text()")
            item_list[index]["maker"] = maker
            index += 1
            
        index = 0
        all_prices = response.selector.xpath("//li/descendant::div[@class='a-column a-span7']/div/a/span[2]")
        for each_price in all_prices:
            price = support.extract_xpath (each_price, "text()")
            try:
                item_list[index]["price"] = price
                index += 1
            except:
                pass
        
        global return_parse_amazon_pages
        return_parse_amazon_pages = item_list

#xpath detection for article
article_identifier = {
        "azure.microsoft.com": "article",
        "www.networkworld.com" : "div[@itemprop='articleBody']",
        "arstechnica.com" : "div[@itemprop='articleBody']",
        "www.theverge.com": "div[@class='c-entry-content']",
        "betanews.com": "div[@class='body clearfix']",
        "aws.amazon.com": "article",
        "www.engadget.com": "article",
        "realm.io": "div[@class='col-xs-12 col-sm-10 col-sm-offset-1 content']",
        "www.viva64.com": "div[@class='item_text2']",
        "www.nojitter.com": "div[@class='text']",
        "techcrunch.com": "div[@class='article-entry text']",
        "www.theregister.co.uk": "div[@id='body']",
        "sdtimes.com": "div[@class='col-md-8 dmbs-main col-xs-12 col-sm-7 hnews hentry item']"
    }