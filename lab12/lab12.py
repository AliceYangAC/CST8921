import os
import uuid
from openai import OpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=f"{os.getenv('AZURE_OPENAI_ENDPOINT').rstrip('/')}/openai/v1/"
)

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

def get_embedding(text):
    response = openai_client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL_DEPLOYMENT"),
        input=text
    )
    return response.data[0].embedding

def chunk_text(text, chunk_size=800):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size
    return chunks


# module 6 embed & upload

def run_upload():
    documents = [
        {"filename": "vacation-policy.txt",   "title": "Employee Vacation Policy",   "category": "vacation"},
        {"filename": "remote-work-policy.txt", "title": "Remote Work Policy",         "category": "remote-work"},
        {"filename": "benefits-overview.txt",  "title": "Employee Benefits Overview", "category": "benefits"}
    ]

    all_chunks = []

    for doc in documents:
        print(f"Processing {doc['filename']}...")
        with open(doc["filename"], "r", encoding="latin-1") as f:
            text = f.read()

        chunks = chunk_text(text)
        print(f"  -> {len(chunks)} chunk(s) created")

        for i, chunk in enumerate(chunks):
            print(f"  -> Generating embedding for chunk {i + 1}...")
            vector = get_embedding(chunk)
            all_chunks.append({
                "id": str(uuid.uuid4()),
                "title": doc["title"],
                "content": chunk,
                "category": doc["category"],
                "sourceFile": doc["filename"],
                "contentVector": vector
            })

    print(f"\nUploading {len(all_chunks)} document chunk(s) to Azure AI Search...")
    result = search_client.upload_documents(documents=all_chunks)
    print(f"Upload complete. {len(result)} result(s) returned.")
    for r in result:
        print(f"  id={r.key} | succeeded={r.succeeded}")


# module 7 search

def run_search():
    query = "vacation carryover"

    # A. Keyword Search
    print("=" * 50)
    print("A. KEYWORD SEARCH")
    print("=" * 50)
    results = search_client.search(search_text=query)
    for r in results:
        print(f"Title: {r['title']}")
        print(f"Content: {r['content'][:200]}")
        print()

    # B. Vector Search
    print("=" * 50)
    print("B. VECTOR SEARCH")
    print("=" * 50)
    query_vector = get_embedding(query)
    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=3,
        fields="contentVector"
    )
    results = search_client.search(search_text=None, vector_queries=[vector_query])
    for r in results:
        print(f"Title: {r['title']}")
        print(f"Content: {r['content'][:200]}")
        print()

    # C. Hybrid Search
    print("=" * 50)
    print("C. HYBRID SEARCH")
    print("=" * 50)
    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query]
    )
    for r in results:
        print(f"Title: {r['title']}")
        print(f"Content: {r['content'][:200]}")
        print()


# module 8 RAG

def ask_llm(question, context_chunks):
    context = "\n\n".join(context_chunks)
    response = openai_client.chat.completions.create(
        model=os.getenv("CHAT_MODEL_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You answer only from supplied context and avoid making up facts."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    return response.choices[0].message.content

def run_rag(question):
    print("=" * 50)
    print(f"Question: {question}")
    print("=" * 50)

    query_vector = get_embedding(question)
    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=3,
        fields="contentVector"
    )

    results = search_client.search(search_text=None, vector_queries=[vector_query])
    chunks = []
    print("Retrieved chunks:")
    for r in results:
        print(f"  - [{r['sourceFile']}] {r['content'][:150]}")
        chunks.append(r["content"])

    print()
    answer = ask_llm(question, chunks)
    print(f"Answer: {answer}")
    print()

if __name__ == "__main__":
    print("Select a module to run:")
    print("  1 - Module 6: Upload & Embed Documents")
    print("  2 - Module 7: Search Queries")
    print("  3 - Module 8: RAG (both questions)")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        run_upload()
    elif choice == "2":
        run_search()
    elif choice == "3":
        run_rag("How many vacation days do employees receive after 5 years?")
        run_rag("What is the remote work policy?")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")