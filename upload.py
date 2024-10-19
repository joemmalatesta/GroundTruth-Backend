import os
import requests
import base64
import chromadb
from sentence_transformers import SentenceTransformer

def get_github_contents(repo_owner, repo_name, path='', token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_file_content(file_url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    return base64.b64decode(response.json()['content']).decode('utf-8')

def process_repo(repo_owner, repo_name, start_path, token=None, chroma_client=None, embedding_model=None):
    contents = get_github_contents(repo_owner, repo_name, path=start_path, token=token)
    
    for item in contents:
        if item['type'] == 'dir':
            process_repo(repo_owner, repo_name, item['path'], token, chroma_client, embedding_model)
        elif item['type'] == 'file':
            file_content = get_file_content(item['download_url'], token=token)
            file_path = f"{repo_owner}/{repo_name}/{item['path']}"
            
            # Generate embedding
            embedding = embedding_model.encode(file_content)
            
            # Add to Chroma
            chroma_client.add(
                embeddings=[embedding.tolist()],
                documents=[file_content],
                metadatas=[{"file_path": file_path}],
                ids=[file_path]
            )
            print(f"Added {file_path} to Chroma database")

if __name__ == '__main__':
    repo_owner = 'owner_username'
    repo_name = 'repository_name'
    start_path = 'src'  # Start from the /src directory
    github_token = os.getenv('GITHUB_TOKEN')
    
    # Initialize Chroma client
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="github_code")
    
    # Initialize embedding model
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    process_repo(repo_owner, repo_name, start_path, token=github_token, chroma_client=collection, embedding_model=embedding_model)
    print("Repository processed and added to Chroma database")
