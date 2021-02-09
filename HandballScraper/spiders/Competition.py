import scrapy
from scrapy_splash import SplashRequest

from ..items import CompetitionItem

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


def extract_last_from_url(url):
    url_split = url.split('/')
    level_brut = url_split[-1]
    level = level_brut.strip()\
        .replace('regions', 'régional')\
        .replace('departements', 'départemental')\
        .replace('coupe-de-france', 'national').strip()
    return level


class CompetitionSpider(scrapy.Spider):
    name = "competition"
    allowed_domains = ['ffhandball.fr']
    start_urls = [
        'https://www.ffhandball.fr/fr/competitions/national',
        'https://www.ffhandball.fr/fr/competitions/regions',
        'https://www.ffhandball.fr/fr/competitions/departements',
        'https://www.ffhandball.fr/fr/competitions/coupe-de-france'
    ]

    child_num = 1
    script = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(2))
            return {
                html = splash:html()
            }
        end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': self.script})


    def parse(self, response):
        level = extract_last_from_url(response.url)
        rows = response.css('.s-tournaments-row')

        # games = response.css('.s-fixtures-table-row__wrapper').extract()
        items = CompetitionItem()
        for row in rows:
            competition_name_list = row.css('.s-tournaments-cell::text').extract()
            competition_name_list_to_str = ' - '.join(competition_name_list)
            competition_name = competition_name_list_to_str.strip()

            competition_link_list = row.css('a::attr(href)').extract()

            competition_id_ffh = extract_last_from_url(competition_link_list[0])
            # Competition ================================
            items['competition_name'] = competition_name
            items['competition_level'] = level
            items['competition_id_ffh'] = competition_id_ffh

            yield items
