import os

from dotenv import load_dotenv
from pinecone import Pinecone
from pymongo import MongoClient

load_dotenv()


class Database:
    def __init__(self, pinecone_api, vec_db_host, mongo_collection, mongo_host):
        self.vec_index = Pinecone(api_key=pinecone_api).Index(host=vec_db_host)
        self.mongo_collection = MongoClient(mongo_host)["richie-brain"][
            mongo_collection
        ]
        print(f"Connected to MongoDB collection: {mongo_collection} at {mongo_host}")

    def search_in_vector_index(
        self,
        query: str,
        namespace: str = "project_summaries",
        top_k: int = 100,
        fields: list = None,
    ):
        return self.vec_index.search(
            namespace=namespace,
            query={"inputs": {"text": query}, "top_k": top_k},
            fields=fields or ["repo_name"],
        )

    def get_repo_summaries(self, repo_list: list):
        print(repo_list)
        return list(self.mongo_collection.find({"repo_name": {"$in": repo_list}}))

    def search(
        self, query: str, namespace: str = "project-summaries", top_k: int = 100
    ):
        results = self.search_in_vector_index(query, namespace, top_k)
        unique_repos = set()
        for r in results["result"]["hits"]:
            unique_repos.add(r["fields"]["repo_name"])
        print(f"Found {len(unique_repos)} unique repositories for query: {query}")
        summaries = self.get_repo_summaries(list(unique_repos))
        if not summaries:
            print("No summaries found for the given repositories.")
            return []
        else:
            return self.get_prompt_context(summaries)

    def get_prompt_context(self, summaries: list) -> str:
        context = []
        for summary in summaries:
            context.append(
                f"""### Repository: {summary['repo_name']}\nLink: https://www.github.com/rishitoshsingh/{summary['repo_name']}\nSummary: {summary['repo_summary']}"""
            )
        return "\n\n".join(context)


if __name__ == "__main__":
    print(os.getenv("PINECONE_API"))
    richi_db = Database(
        pinecone_api=os.getenv("PINECONE_API"),
        vec_db_host=os.getenv("PINECONE_INDEX"),
        mongo_collection="project-summaries",
        mongo_host=os.getenv("MONGODB_HOST"),
    )
    print(richi_db.search("Does the candidate have experience with pytorch?"))
