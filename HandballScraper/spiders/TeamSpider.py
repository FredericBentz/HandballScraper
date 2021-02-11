import scrapy
from scrapy_splash import SplashRequest

from ..items import HandballscraperItem

script = """
    function main(splash, args)
        child_num = 1
        assert(splash:go(args.url))
        assert(splash:wait(2))
        local element = splash:select('.s-fixtures-calendar-day:nth-child('.. child_num ..')')
        local bounds = element:bounds()
        assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
        return html = splash:html()
    end
"""


class HandballSpider(scrapy.Spider):
    name = "handball"
    allowed_domains = ['ffhandball.fr']
    start_urls = ['https://www.ffhandball.fr/fr/competition/15604#poule-78106']

    child_num = 1
    script = """
        function main(splash, args)
            child_num = 1
            assert(splash:go(args.url))
            assert(splash:wait(2))
            local element = splash:select('.s-fixtures-calendar-day:nth-child('.. child_num ..')')
            local bounds = element:bounds()
            assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
            return {
                html = splash:html(),
            }
end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': self.script})
            # yield SplashRequest(url,
            #                     self.parse,
            #                     endpoint='render.html',
            #                     args={'wait': 2},
            #                     )

    def parse(self, response):
        teams = response.css('.s-standings-cell--name::text').extract()
        # games = response.css('.s-fixtures-table-row__wrapper').extract()
        items = HandballscraperItem()
        for team in teams:
            # Team ================================
            team_name = team
            items['team_name'] = team_name
            yield items

