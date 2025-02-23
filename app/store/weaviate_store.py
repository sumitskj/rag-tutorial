import weaviate

from weaviate.collections.classes.config import Configure
from weaviate.collections.classes.grpc import MetadataQuery

from app.configs import OPENAI_KEY
from app.logging import logger


class Weaviate():
    def __init__(self):
        super().__init__()
        collections = ["Documents"]
        client = self.get_client()
        for collection in collections:
            if not client.collections.exists(collection):
                client.collections.create(
                    name=collection,
                    vectorizer_config=Configure.Vectorizer.text2vec_openai(
                        model="text-embedding-3-large"
                    ),
                    multi_tenancy_config=Configure.multi_tenancy(enabled=False)
                )
                logger.info(f"Created collection : {collection}")
        client.close()

    def get_client(self):
        client = weaviate.connect_to_local(headers={"X-OpenAI-Api-Key": OPENAI_KEY}, )
        return client

    def insert(self, data: list, collection_name: str):
        client = self.get_client()
        try:
            collection = client.collections.get(collection_name)
            with collection.batch.dynamic() as batch:
                for d in data:
                    batch.add_object(properties=d)
                    logger.info(f"Added object: {d['file_name']} {d['page_no']}")

            if len(collection.batch.failed_objects) > 0:
                for e in collection.batch.failed_objects:
                    logger.error(f"Insert failed: {e}")
        finally:
            if client:
                client.close()

    def search(self, query: str, collection_name: str):
        client = self.get_client()
        try:
            collection = client.collections.get(collection_name)
            response = collection.query.near_text(
                query=query,
                distance=0.7,
                limit=10,
                return_metadata=MetadataQuery(distance=True),
            )
            return [obj.properties for obj in response.objects]
        finally:
            if client:
                client.close()
