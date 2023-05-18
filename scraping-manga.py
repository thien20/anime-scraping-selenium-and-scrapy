import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.settings import Settings



class AnimeSpider(CrawlSpider):
    name = 'myanimelist'
    allowed_domains = ['myanimelist.net']
    start_urls = ['https://myanimelist.net/topmanga.php?type=manga&limit=0']
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 0.5,
    # }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_link)

    def parse_link(self,response):
        next_page = response.xpath('//a[text()="Next 50"]/@href').get()

        for link in response.css('.ranking-list td.title a::attr(href)').getall():
            yield response.follow(link, callback=self.parse_anime_info)
        # Instead of using "follow", the choice of Request is much better for handle all elements in 1 page
        # Using follow may cause turn to next_page during scraping those elements, while Request reduces it
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse_link)
        # if next_page:
        #     url = response.urljoin(next_page)
        #     yield response.follow(url, callback=self.parse_link)
        
            
            
            
    def parse_anime_info(self,response):
        yield{
            'name': response.css('span.h1-title ::text').get(),
            'type':  response.xpath('//span[text()="Type:"]/following-sibling::a/text()').getall(),
            'volumes':  response.xpath('//span[text()="Volumes:"]/following-sibling::text()').get(),
            'chapters': response.xpath('//span[text()="Chapters:"]/following-sibling::text()').get(),
            'status': response.xpath('//span[text()="Status:"]/following-sibling::text()').get(),
            'time_published': response.xpath('//span[text()="Published:"]/following-sibling::text()').get(),
            'genres': response.xpath('//span[text()="Genres:"]/following-sibling::span/text()').getall(),
            'theme': response.xpath('//span[text()="Themes:"]/following-sibling::span/text()').getall(),
            'demographic': response.xpath('//span[text()="Demographic:"]/following-sibling::span/text()').getall(),
            'serialization': response.xpath('//span[text()="Serialization:"]/following-sibling::a/text()').getall(),

            'score': response.xpath('//span[text()="Score:"]/following-sibling::span/span/text()').getall(),
            'ranked': response.xpath('//span[text()="Ranked:"]/following-sibling::text()').get(),
            'popularity': response.xpath('//span[text()="Popularity:"]/following-sibling::text()').get(),
            'members': response.xpath('//span[text()="Members:"]/following-sibling::text()').get(),
            'favorites': response.xpath('//span[text()="Favorites:"]/following-sibling::text()').get(),
        }
        
        
