import requests
import base64
import os

def get_github_contents(repo_owner, repo_name, path='', token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_file(file_url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    return base64.b64decode(response.json()['content']).decode('utf-8')

def download_repo(repo_owner, repo_name, local_path='', token=None):
    contents = get_github_contents(repo_owner, repo_name, token=token)
    
    for item in contents:
        if item['type'] == 'dir':
            new_path = os.path.join(local_path, item['name'])
            os.makedirs(new_path, exist_ok=True)
            download_repo(repo_owner, repo_name, path=item['path'], local_path=new_path, token=token)
        elif item['type'] == 'file':
            file_content = download_file(item['download_url'], token=token)
            file_path = os.path.join(local_path, item['name'])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

if __name__ == '__main__':
    repo_owner = 'owner_username'
    repo_name = 'repository_name'
    local_path = 'downloaded_repo'
    github_token = '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'  # Optional, but recommended for private repos or to avoid rate limits
    
    download_repo(repo_owner, repo_name, local_path, token=github_token)
    print(f"Repository downloaded to {local_path}")

