from pathlib import Path

import fitz

from app.logging import logger
from app.store.weaviate_store import Weaviate


def vectorize():
    cms_path = Path("/cms")
    if not cms_path.exists() or not cms_path.is_dir():
        logger.error(f"cmspath is invalid {cms_path}")
        raise Exception(f"cmspath is invalid {cms_path}")

    files = [{"file_path": file} for file in cms_path.rglob("*") if file.is_file()]
    weaviate_client = Weaviate()
    for file in files:
        file_path = file["file_path"]
        doc = fitz.open(file_path.resolve())
        content = []

        for ind, page in enumerate(doc):
            text_data = page.get_text("text")
            content.append({"page_no": ind, "file_name": file_path.name, "data": text_data})
        weaviate_client.insert(data=content, collection_name="Documents")
        # logger.info(f"File content : {content}")
    logger.info("Vectorization complete")
