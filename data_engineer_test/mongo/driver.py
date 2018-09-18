"""
Access  mongo
"""

import pymongo
import sys

class MongoDriver():
    connection_string = "mongodb://isentiaUser:isentiatest@portal-ssl394-5.isentia-test.3021464179.composedb.com:20340,portal-ssl364-0.isentia-test.3021464179.composedb.com:20340/compose?authSource=admin&ssl=true"

    
    def __get_client(self):
        try:
            connection = pymongo.MongoClient(self.connection_string)
            print ("Connection returned successfully")
            return connection
        except:
            print ("Could not connect to MongoDB: %s" % sys.exc_info()[0])
            raise

    def __get_collection(self, connection):
        db = connection.crawlDb
        collection = db.scrappyResults
        return collection
        
    def insert_article(self, article):
        conn = self.__get_client()
        try:
            collection = self.__get_collection(conn)
            return collection.insert_one(article).inserted_id
        finally:
            conn.close()

    def search_article_by_title(self, title):
        conn = self.__get_client()
        try:
            article_list = list()
            collection = self.__get_collection(conn)
            articles = collection.find({"title" : "/%s/" % title})
            for article in articles:
                article_list.append(article)

            return article_list
        finally:
            conn.close()

    def search_article_by_content(self, content):
        conn = self.__get_client()
        try:
            article_list = list()
            collection = self.__get_collection(conn)
            articles = collection.find({"content" : "/%s/" % content})
            for article in articles:
                article_list.append(article)

            return article_list
        finally:
            conn.close()

    def search_article(self, text):
        article_list = list()
        result_search_content = self.search_article_by_content(text)
        result_search_title = self.search_article_by_title(text)
        
        for article in result_search_content:
            article_list.append(article)

        for article in result_search_title:
            if article not in article_list:
                article_list.append(article)

        return article_list

    def truncate_database(self):
        conn = self.__get_client()
        try:
            collection = self.__get_collection(conn)
            collection.delete_many({})
        finally:
            conn.close()
