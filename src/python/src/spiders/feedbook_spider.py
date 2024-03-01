from typing import Any
import logging
import scrapy
from scrapy.http import Response

from items.feedbook_item import FeedbookItem


class FeedbookSpider(scrapy.Spider):
    name = 'feedbook'
    allowed_domains = ['feedbooks.com']
    start_urls = ['https://www.feedbooks.com/search?advanced_search=true&age=all&author=&award=&book_format=all&button=&collection_name=&description=&lang=all&publication_date_end=&publication_date_start=&publisher_name=&query=&serie=&title=']

    proxy_enabled = True

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
        logging.info(book)