import os

from pinecone import Pinecone
from pymongo import MongoClient


class Database:
    def __init__(self, pinecone_api, vec_db_host, mongo_collection, mongo_host):
        self.vec_index = Pinecone(api_key=pinecone_api).Index(host=vec_db_host)
        self.mongo_collection = MongoClient(mongo_host)["richie-brain"][
            mongo_collection
        ]

    def insert_record(self, record):
        self.mongo_collection.insert_one(
            {
                "repo_name": record["repo_name"],
                "repo_summary": record["repo_summary"],
            }
        )
