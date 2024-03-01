import logging
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class FeedbookImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'image_name': item["image_name"]})
                for x in item.get('image_link')]

    def file_path(self, request, response=None, info=None):
        return request.meta['image_name']