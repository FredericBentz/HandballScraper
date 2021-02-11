from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# configure_logging()
# runner = CrawlerRunner()
#
#
# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl('reunion')
#     yield runner.crawl('partant')
#     reactor.stop()
#
#
# crawl()
# reactor.run() # the script will block here until the last crawl call is finished
configure_logging()
process = CrawlerProcess(get_project_settings())


@defer.inlineCallbacks
def crawl():
    # yield process.crawl('reunion')
    yield process.crawl('competition')
    # yield process.crawl('partant')
    # yield process.crawl('resultat')
    # yield process.crawl('rapportPMU')
    # yield process.crawl('rapportPMUe')
    # yield process.crawl('rapportLeTurf')
    # yield process.crawl('rapportGeny')
    reactor.stop()  # process.start() # the script will block here until all crawling jobs are finished


crawl()
reactor.run()