import scrapy
from ..items import EfinancialItem

class Jobs(scrapy.Spider):
    name = 'efinancial'
    end_page = None
    start_page = input('Enter Your Start Range :  ')
    dump = input('Do You Want To Using End Limit [Y/N] :  ')
    if dump[0].upper() == 'Y':
        end_page = int(input('Enter Your End Range :  '))
    if int(start_page) == 1:
        start_urls = [
            'https://www.efinancialcareers.hk/jobs-Technology.s019',
        ]
    else:
        start_urls = [
            f'https://www.efinancialcareers.hk/jobs-Technology.s019?jobSearchId=NTBGNDI2MjA2RUU0QjJDNUY1QTEzMDg2ODBGMDQ5NjEuMTY0NDM3ODEwMjE2Mi4xNDU2MjU2NjY0&page={start_page}',
        ]
    def parse(self, response):
        cards = response.css('.well')
        month_dict = {'Jan':'01','Feb': '02','Mar':'03','Apr': '04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        for card in cards:
            item = EfinancialItem()
            _id = card.css('a.anchor::attr(id)').extract()[0][3:]
            url = card.css('a::attr(href)').extract()[0]
            company = card.css('.company span::text').extract()[1]
            date = str(card.css('.updated span::text').extract())[-10:-2].split(' ')
            if len(date[0]) is 2:
                date = f'20{date[2]}-{month_dict[date[1]]}-{date[0]}'
            else:
                date = f'20{date[2]}-{month_dict[date[1]]}-0{date[0]}'
            work = card.css('a span::text').extract()[0]
            price = card.css('.salary span::text').extract()[0]
            # Passing Data To Item
            item['_id'] = _id
            item['url'] = url
            item['Company'] = company
            item['date'] = date
            item['work'] = work
            item['price'] = price
            yield item
        # Preparing CallBack Functionality
        next_page = response.css('a.nextPage::attr(href)').get()
        if next_page is not None:# Check If Value is Null
            if self.end_page is None:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )
            else:
                st = int(next_page.split('page=')[-1])
                # yield {'val' : st}
                if st <= self.end_page: # Check Page Limit Described
                    yield scrapy.Request(
                        response.urljoin(next_page),
                        callback=self.parse
                    )