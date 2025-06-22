import os

import openai
from pinecone import Pinecone
from pymongo import MongoClient

from rag.graph.consts import PROJECT_RETREIVE_NAMESPACE, RESUME_RETREIVE_NAMESPACE


class Database:
    def __init__(
        self, pinecone_api, vec_db_host, mongo_database, mongo_collection, mongo_host
    ):
        self.vec_index = Pinecone(api_key=pinecone_api).Index(host=vec_db_host)
        self.mongo_collection = MongoClient(mongo_host)[mongo_database][
            mongo_collection
        ]

    def get_embedding(self, text: str) -> list:
        res = openai.embeddings.create(input=[text], model="text-embedding-3-small")
        return res.data[0].embedding

    def search_in_vector_index(
        self,
        vector: list,
        namespace: str = "project_summaries",
        top_k: int = 20,
    ):
        return self.vec_index.query(
            namespace=namespace,
            vector=vector,
            top_k=top_k,
            include_values=False,
            include_metadata=True,
        )

    def get_repo_summaries(self, repo_list: list):
        return list(self.mongo_collection.find({"repo_name": {"$in": repo_list}}))

    def search(self, query: str, namespace: str, top_k: int = 5):
        if namespace == PROJECT_RETREIVE_NAMESPACE:
            results = self.search_in_vector_index(
                vector=self.get_embedding(query), namespace=namespace, top_k=top_k
            )
            # print(results)

            unique_repos = set()
            for matches in results["matches"]:
                unique_repos.add(matches["metadata"]["repo_name"])
            summaries = self.get_repo_summaries(list(unique_repos))
            if not summaries:
                print("No summaries found for the given repositories.")
                return "No documents found"
            else:
                return self._get_project_context(summaries)
        elif namespace == RESUME_RETREIVE_NAMESPACE:
            results = self.search_in_vector_index(
                vector=self.get_embedding(query), namespace=namespace, top_k=top_k
            )
            # print(results)
            documents = []
            for matches in results["matches"]:
                documents.append(matches["metadata"]["text"])
            if not documents:
                print("No resume document found")
                return "No documents found"
            else:
                return "\n\n".join(documents)

    def _get_project_context(self, summaries: list) -> str:
        context = []
        for summary in summaries:
            context.append(
                f"""### Repository: {summary['repo_name']}\nLink: https://www.github.com/rishitoshsingh/{summary['repo_name']}\nSummary: {summary['repo_summary']}"""
            )
        return "\n\n".join(context)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    print(os.getenv("PINECONE_API"))
    richi_db = Database(
        pinecone_api=os.getenv("PINECONE_API"),
        vec_db_host=os.getenv("PINECONE_INDEX_DEV"),
        mongo_database="richie-dev",
        mongo_collection="project-analysis",
        mongo_host=os.getenv("MONGODB_HOST"),
    )
    print(
        richi_db.search(
            "Show me his projects?",
            PROJECT_RETREIVE_NAMESPACE,
        )
    )
