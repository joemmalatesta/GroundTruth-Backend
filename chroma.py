import csv
import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Initialize OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

# Initialize Chroma client with persistence
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get the collection
collection = client.get_or_create_collection(name="sentry_docs", embedding_function=openai_ef)

# Read the CSV file and add documents if the collection is empty
if collection.count() == 0:
    with open('sentryDocs.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Read the content of the text file from sentrydocs directory
            summary_path = os.path.join('sentrydocs', row['summary'].strip())
            with open(summary_path, 'r') as textfile:
                content = textfile.read()
            
            # Add the document to the collection
            collection.add(
                documents=[content],
                metadatas=[{"type": row['type'].strip(), "title": row['title'].strip(), "url": row['url'].strip()}],
                ids=[row['id'].strip()]
            )

    print("Embedding process completed.")
else:
    print("Collection already exists and is not empty. Skipping embedding process.")

# Test query
query = "User Feedback"
results = collection.query(
    query_texts=[query],
    n_results=1,
    include=["metadatas"]
)

if results['metadatas']:
    closest_title = results['metadatas'][0][0]['title']
    print(f"The closest match to '{query}' is: {closest_title}")
else:
    print("No results found.")
