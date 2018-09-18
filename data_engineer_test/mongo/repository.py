# -*- coding: utf-8 -*-
"""
Provides access to mongo from API Gateway
"""

from data_engineer_test import mongo

def search_article(text):
    mongo_driver = mongo.driver.MongoDriver()
    return mongo_driver.search_article(text)