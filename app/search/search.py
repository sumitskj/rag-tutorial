from app.configs import OPENAI_KEY
from app.store.weaviate_store import Weaviate
from openai import OpenAI


def search(query):
    # genai + info vd
    weaviate_client = Weaviate()
    relevant_docs = weaviate_client.search(query=query, collection_name="Documents")

    prompt = f"""A user has asked this query. Please answer it using all the information that will be provided to you. 
        Also in the response mention the file source from which you have found this information. 
        Query: {query}\n Data related to the question where you have to look for the answer: {relevant_docs}"""

    open_ai_client = OpenAI(api_key=OPENAI_KEY)
    completion = open_ai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an helpful assistant that answers all the queries that are asked to you.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return {"answer": completion.choices[0].message.content}
