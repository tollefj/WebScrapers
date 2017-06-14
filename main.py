import mechanicalsoup
import os
import re
import lxml.etree
from slugify import slugify

class Fund():
    def __init__(self,name=''):
        self.name = name

    def get_name(self):
        return self.name

class ScrapeFunds():
    def __init__(self):
        print 'starting scraper'
        self.url = 'https://www.skagenfondene.no'
        self.browser = None
        self.page = None
        self.init_browser()

    def access_page(self,url):
        self.browser.open(url)
        return self.browser.get_current_page()

    def init_browser(self):
        try:
            self.browser = mechanicalsoup.StatefulBrowser(
                soup_config={'features': 'lxml'}
            )
            self.page = self.access_page(self.url+'/fond')
            self.locate_equity_funds()
        except Exception:
            raise

    def locate_equity_funds(self):
        equity_holdings = dict()

        equity_funds = self.page.find('div',id='fund-tiles-12006')
        for equity in equity_funds.find_all('a',href=True):
            endpoint = self.url + equity['href']
            print endpoint
            # access fund page's investments portfolio
            endpoint_page = self.access_page(endpoint + 'portefoljeoversikt')
            # for categories in endpoint_page.find_all('h3'):
            #     c = slugify(categories.text).encode('utf-8')
            fund_name = endpoint_page.find('b',class_='asof').text.split('pr')[0].strip()
            print '\n******************'+fund_name+'******************\n'
            for table in endpoint_page.find_all('div',class_='no-more-tables'):
                table_title = table.find('h3').text

                if table_title.lower().startswith('sum'):
                    continue
                else:
                    print '\n##################'+table_title+'##################\n'

                    for column in table.find_all('tr'):
                        idx = 0
                        comp_name = None
                        comp_link = None
                        comp_holdings = None
                        for values in column.find_all('td'):
                            val = values.text.strip()
                            if 'sum' not in val.lower():
                                try:
                                    _comp = values.find('a')
                                    comp_name = _comp.text
                                    comp_link = _comp['href']
                                except Exception:
                                    pass
                                if '%' in val:
                                    comp_holdings = val.split()[0]
                        if not comp_name and comp_holdings:
                            # this is the sum of the section
                            comp_name = table_title + ' Sum'
                        if comp_name and comp_holdings:
                            print comp_name, comp_link, comp_holdings
                print '\n---------------------------------------------\n'
            print '\n**********************************************n'


    def run(self):
        pass

if __name__ == "__main__":
    s = ScrapeFunds()
