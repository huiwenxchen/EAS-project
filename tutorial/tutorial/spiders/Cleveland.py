# import scrapy

# class QuotesSpider(scrapy.Spider):
#     name = "cleveland" 
    
#     start_urls = ['https://www.clevelandart.org/art/collection/search?i=1&sort-results=accession_number_sortable+desc&filter-department=Chinese+Art&limit=2516']

#     print('start_url')

#     def parse(self, response):
#         # art_list = response.css("tbody tr")
#         art_list = response.css('div.masonry-grid')
#         print('LENGTH', len(art_list))
#         for art in art_list:
#             art_link = art.css('div.thumbnail a::attr(href)').get()
#             if art_link:
#                 link = 'https://www.clevelandart.org/' + art_link
#                 yield response.follow(link, callback=self.parse_art)


#     def parse_art(self, response):
#         """
#         scrape art pieces
#         """
#         yield {
#             'title': response.css('div.pane-content h1.field-name-field-primary-title::text').get(),
#             'artist_name': response.css('div.pane-content div.field-name-art-object-artists a::text').get(),
#             'artist_date': response.css('div.pane-content div.field-name-art-object-artists p.field-name-field-artist-origin::text').get(),
#             'artwork_date': response.css('div.pane-content p.field-name-field-date-text::text').get(),
#             'accession_num': response.css('div.pane-content span.field-name-field-accession-number::text').get(),
#             "art_medium": response.css('div.pane-content p.field-name-art-object-medium::text').get(),
#             'info_link': response.css('meta[property="og:url"]::attr(content)').get(),
#             'img_link': response.css('div.view-content span.field-content img::attr(data-src)').get(),
#         }

#         #             # yield {
# #             #     'title': response.css('div.w860 h1::text').get(),
# #             #     'date': response.css('div.origin span::text').get(),
# #             #     'artist': response.css('tbody tr div.artists::text').get()
# #             #     'link': base_url + response.css('tbody tr a::attr(href)')
# #             #     'img_link': response.css('tbody tr img::attr(data-src)').get()
# #             #     'alt': response.css('tbody tr img::attr(alt)').get()
# #             # }
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = '/Applications/Google Chrome.app/'
driver = webdriver.Chrome(chrome_options=chrome_options)

class QuotesSpider(scrapy.Spider):
    name = "cleveland"
    
    start_urls = ['https://www.clevelandart.org/art/collection/search?i=1&sort-results=accession_number_sortable+desc&filter-department=Chinese+Art&limit=2516']

    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome()

    def parse(self, response):
        # Load the page using the Selenium driver
        self.driver.get(response.url)

        # Scroll down to load all items on the page
        for i in range(10):
            time.sleep(2)
            self.logger.info('Scrolling down...')
            self.driver.find_element_by_tag_name('html').send_keys(Keys.END)

        # Scrape the data from the fully loaded page
        art_list = response.css('div.masonry-grid')
        for art in art_list:
            art_link = art.css('div.thumbnail a::attr(href)').get()
            if art_link:
                link = 'https://www.clevelandart.org/' + art_link
                yield response.follow(link, callback=self.parse_art)

    def parse_art(self, response):
        """
        scrape art pieces
        """
        yield {
            'title': response.css('div.pane-content h1.field-name-field-primary-title::text').get(),
            'artist_name': response.css('div.pane-content div.field-name-art-object-artists a::text').get(),
            'artist_date': response.css('div.pane-content div.field-name-art-object-artists p.field-name-field-artist-origin::text').get(),
            'artwork_date': response.css('div.pane-content p.field-name-field-date-text::text').get(),
            'accession_num': response.css('div.pane-content span.field-name-field-accession-number::text').get(),
            "art_medium": response.css('div.pane-content p.field-name-art-object-medium::text').get(),
            'info_link': response.css('meta[property="og:url"]::attr(content)').get(),
            'img_link': response.css('div.view-content span.field-content img::attr(data-src)').get(),
        }




