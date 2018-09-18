# -*- coding: utf-8 -*-
"""
Provides access to mongo from API Gateway
"""

from data_engineer_test.mongo import driver

def search_article(text):
    mongo_driver = driver.MongoDriver()
    return mongo_driver.search_article(text)


    
if __name__ == '__main__':
    #ensure the file exists on the lambda finction
    results = search_article("trump")
    print(results)