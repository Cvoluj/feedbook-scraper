import logging
import scrapy
from scrapy.http import Response
from scrapy.exceptions import DontCloseSpider
from scrapy import signals
from datetime import datetime, timedelta

from items.feedbook_item import FeedbookItem


class FeedbookSpider(scrapy.Spider):
    name = 'feedbook'
    allowed_domains = ['feedbooks.com']

    proxy_enabled = False
    proxy_mode = 1
    
    ## method to generate links from time - time, without overlapping
    @staticmethod
    def generate_links_period(start_date: datetime, end_date: datetime, delta: int):
        base_url = "https://www.feedbooks.com/search?advanced_search=true&age=all&author=&award=&book_format=all&button=&collection_name=&description=&lang=all&publication_date_end={end_date}&publication_date_start={start_date}&publisher_name=&query=&serie=&sort=recent&title="
        links = []
        while start_date <= end_date:
            next_date = start_date + timedelta(days=delta)
            end_date_str = min(next_date - timedelta(days=1), end_date).strftime("%Y-%m-%d")
            link = base_url.format(start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date_str)
            links.append(link)
            start_date = next_date
        return links  

    ## 0000-1954 ~9500 books
    from_jesus_birth = ['https://www.feedbooks.com/search?advanced_search=true&age=all&author=&award=&book_format=all&button=&collection_name=&description=&lang=all&publication_date_end=1954-01-01&publication_date_start=0000-01-01&publisher_name=&query=&serie=&title=']
    ## from this 5 year period there are no links with >1000 books
    links1954_1993 = generate_links_period(datetime(1954, 1, 2), datetime(1993, 12, 22), 365 * 5)
    ## 14 day period, because from ~2017 there are ~3000 books in 2 weeks
    links1993_today = generate_links_period(datetime(1993, 12, 23), datetime.today(), 14)

    # testlink = generate_links_period(datetime(1993, 8, 23), datetime(1993, 12, 23), 14)
    # *from_jesus_birth, *links1954_1993, *links1993_today
    start_urls = [*from_jesus_birth, *links1954_1993, *links1993_today]
   
    def parse(self, response: Response):
        for book in response.css('div.browse__item'):

            book_small_url = book.css('a.block__item-title::attr(href)').get()
            book_full_url = response.urljoin(book_small_url)

            yield scrapy.Request(book_full_url, callback=self.parse_book)

        next_page = response.css('a.pagination__navigator[data-post-hog="catalog-changepage-next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book(self, response: Response):
        image_name = None
        series = None
        series_number = None
        currency = None
        authors = []
        translators = []

        book_id = response.url.split('/')[-1]
        title = response.css('h1::text').get().strip()

        subtitle_elements = response.css('.item__subtitles .item__subtitle')
        for subtitle_element in subtitle_elements:
            subtitle_text = ' '.join(subtitle_element.css('*::text').getall()).strip()
            authors.append(subtitle_text)

        currency = response.meta.get('currency')
        categories = response.css('.item__chips a[class^="classification-chip"]::text').getall()
        description = response.css('.item__description.tabbed#item-description').xpath('string()').get().strip()
        
        details_dict = {}
        detail_elements = response.css('.item-details__key')
        for element in detail_elements:
            key = element.css('::text').get().strip()
            value_element = element.xpath('./following-sibling::div[@class="item-details__value"][1]')
            value = value_element.css('::text').get().strip()
            if not value:
                value = value_element.css('a::text').get()
            details_dict[key] = value
        publication_date = details_dict.get('Publication date')
        publisher = details_dict.get('Publisher')
        epub_isbn = details_dict.get('EPUB ISBN')
        paper_isbn = details_dict.get('Paper ISBN')
        language = details_dict.get('Language')
        page_count = details_dict.get('Page count')
        format_ebook = details_dict.get('Format')
        ebook_size = details_dict.get('File size')
        protection = details_dict.get('Protection')

        series_link = response.css('.item__subtitles > div.item__subtitle > a.link[href*="/series/"]::attr(href)').get(default=None)
        if series_link:
            series_link = response.urljoin(series_link)
            series = response.css('.item__subtitles > div.item__subtitle > a.link[href*="/series/"]::text').get()
            series_number = response.css('.item__subtitles > div.item__subtitle > span::text').get().strip()[1:]



        price = response.css('.item__buy::text').get()
        image_link = [response.css('.item__cover img::attr(src)').get()]

        book = FeedbookItem(
            book_id=book_id,
            book_url=response.url,
            title=title,
            authors=authors,
            translators=translators,
            series=series,
            series_number=series_number,
            series_link=series_link,
            categories=categories,
            description=description,
            publication_date=publication_date,
            publisher=publisher,
            epub_isbn=epub_isbn,
            paper_isbn=paper_isbn,
            language=language,
            page_count=page_count,
            format_ebook=format_ebook,
            ebook_size=ebook_size,
            protection=protection,
            price=price,
            currency=currency,
            image_link=image_link,
            image_name=image_name
        )
       
        yield book
