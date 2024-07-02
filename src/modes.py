import requests
import os

def fetch_modes(repo_url):
    api_url = f"{repo_url}/contents/patterns"
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_API_KEY")}'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        modes = {item['name']: item['name'] for item in data if item['type'] == 'dir'}
        return modes
    else:
        print(f"[bold red]Failed to fetch modes from repository. Status code: {response.status_code}[/bold red]")
        return {}

def fetch_prompt(repo_url, mode):
    api_url = f"{repo_url}/contents/patterns/{mode}/system.md"
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_API_KEY")}'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        content = requests.get(data['download_url']).text
        return content
    else:
        print(f"[bold red]Failed to fetch prompt for mode '{mode}'. Status code: {response.status_code}[/bold red]")
        return ""
