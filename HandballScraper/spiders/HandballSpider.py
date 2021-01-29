import scrapy

from ..items import HandballscraperItem


class HandballSpider(scrapy.Spider):
    name = "handball"
    allowed_domains = ['ffhandball.fr']

    def start_requests(self):
        urls = [
            'https://www.ffhandball.fr/fr/competition/15603#poule-78325'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        
        page = response.xpath('.m-standings , .m-standings__content')
        teams = page.xpath('.s-standings-cell--name').extract()
        for team in teams:
            team_name = team


            # filename = f'Competition-{teams}.html'
            # with open(filename, 'wb') as f:
            #     f.write(response.body)
            # self.log(f'Saved file {filename}')
            # ITEMS ==============================================
            items = HandballscraperItem()
            # Team ================================
            items['team_name'] = team_name
