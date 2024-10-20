import os
import requests
import base64
import chromadb

def get_github_contents(repo_owner, repo_name, path='', token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_file_content(url, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    print(url)
    response = requests.get(url, headers=headers)
    print(response.text)
    response.raise_for_status()
    content = response.text
    
    
    # Extract filename and path from the URL
    path_parts = url.split('/')
    filename = path_parts[-1]
    path = '/'.join(path_parts[:-1])
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.join('skeleton', 'doc', path), exist_ok=True)
    
    # Save the content to the file
    with open(os.path.join('skeleton', 'doc', path, filename), 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Saved content to skeleton/doc/{path}/{filename}")
    return content


def sanity_check(repo_owner, repo_name, start_path, token=None):
    contents = get_github_contents(repo_owner, repo_name, path=start_path, token=token)
    
    print(f"Contents of {start_path}:")
    for item in contents:
        if item['type'] == 'dir':
            print(f"\nDirectory: {item['name']}")
            try:
                page_svelte = get_github_contents(repo_owner, repo_name, f"{item['path']}/+page.svelte", token=token)
                if isinstance(page_svelte, dict) and page_svelte.get('type') == 'file':
                    print(f"  - Found +page.svelte")
                    content = get_file_content(page_svelte['download_url'], token=token)
                    print(f"  - Content (first 200 characters):\n{content[:200]}...")
                else:
                    print(f"  - No +page.svelte found")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"  - No +page.svelte found")
                else:
                    print(f"  - Error checking for +page.svelte: {e}")
        elif item['type'] == 'file':
            print(f"File: {item['name']}")

if __name__ == '__main__':
    repo_owner = 'skeletonlabs'
    repo_name = 'skeleton'
    start_path = 'sites/skeleton.dev/src/routes/(inner)/components'
    github_token = os.getenv('GITHUB_TOKEN')
    
    sanity_check(repo_owner, repo_name, start_path, token=github_token)
