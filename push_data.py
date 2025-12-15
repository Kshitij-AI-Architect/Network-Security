import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self, file_path):
        """
        This function will convert csv file to json format
        """
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(data.T.to_dict().values())    
            return records       
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongoDB(self, records, database_name, collection_name):
        """
        This function will insert data to mongoDB
        """
        try:
            self.database = database_name
            self.collection = collection_name
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records), "Records inserted successfully")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "KSHITIJ-AI"
    COLLECTION = "NetworkData"
    networkobj=NetworkDataExtract()
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records[0])
    no_of_records = networkobj.insert_data_to_mongoDB(records=records, database_name=DATABASE, collection_name=COLLECTION)
    print(no_of_records)