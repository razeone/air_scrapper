#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Easy scrapper for ingesting data stored in webpages."""

import datetime
import requests
from lxml import html
from pymongo import MongoClient

AIR_REPORT_WEBPAGE = 'http://www.aire.cdmx.gob.mx/ultima-hora-reporte.php'
PAGE = requests.get(AIR_REPORT_WEBPAGE)
TREE = html.fromstring(PAGE.content)


def get_mongo_client():
    client = MongoClient()
    client = MongoClient('mongodb://user:password@localhost:27017/')
    return client['redoxon']


def strip_string(input_string):
    """Removes tabs and car returns from strings."""
    return input_string.replace("\t", "").replace("\n", "")


RESULT_DICT = {
    "air_quality": strip_string(
        TREE.xpath('//div[@id="mensajeimeca"]/h3//text()')[0]),
    "temperature": TREE.xpath('//div[@id="textotemperatura"]//text()')[0],
    "timestamp": '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
}

client = get_mongo_client()
air_collection = client['air_collection']
post_id = air_collection.insert_one(RESULT_DICT).inserted_id

print(post_id)
