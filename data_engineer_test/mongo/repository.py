# -*- coding: utf-8 -*-
"""
Provides access to mongo from API Gateway
"""

from data_engineer_test.mongo import driver

def search_article(text):
    mongo_driver = driver.MongoDriver()
    return mongo_driver.search_article(text)

def truncate_database():
    mongo_driver = driver.MongoDriver()
    mongo_driver.truncate_database()


    
if __name__ == '__main__':
    results = search_article("Apple")
    print(results)