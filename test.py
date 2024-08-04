import requests
import re
import os
from getpass import getpass
import base64

# Configuration
GITHUB_REPO_URL = 'https://github.com/myorg/myrepo'  # Example repository URL
SECRET_KEYWORDS = ['AWS_SECRET', 'GITHUB_TOKEN', 'API_KEY']  # Keywords to search for
TARGET_FILE = 'config/.env'  # Example file to check for secrets

def fetch_repo_files(url):
    """Fetch the content of the files in the GitHub repository."""
    # Note: GitHub API requires authentication for private repos or high request limits.
    # Here, we're assuming the repo is public and files are accessible.
    try:
        response = requests.get(f'{url}/contents/')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch repository files: {e}")
        return []

def search_for_secrets(file_url, keywords):
    """Search for secrets in the given file URL."""
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        content = response.text

        secrets_found = {keyword: re.findall(rf'{keyword}=[^\s\'"]+', content) for keyword in keywords}
        return secrets_found
    except requests.RequestException as e:
        print(f"Failed to fetch file content: {e}")
        return {}

def exploit_secret(secret, keyword):
    """Simulate exploiting a found secret."""
    if keyword == 'AWS_SECRET':
        print(f"Exploiting AWS secret: {secret}")
        # Example: Attempt to use the AWS secret to access an S3 bucket (hypothetical)
        # You would use boto3 or AWS CLI here in a real scenario.
    elif keyword == 'GITHUB_TOKEN':
        print(f"Exploiting GitHub token: {secret}")
        # Example: Use the token to access private repositories or perform actions on GitHub.
        # You would use requests or PyGithub here in a real scenario.
    elif keyword == 'API_KEY':
        print(f"Exploiting API key: {secret}")
        # Example: Use the API key to access a third-party API.
        # You would use requests or another HTTP library here in a real scenario.
    else:
        print(f"Unknown secret type: {secret}")

def main():
    print("Disclaimer: This script is for educational purposes only. Unauthorized use is illegal.")
    
    # Input GitHub repo and target file for demonstration
    repo_url = input("Enter the GitHub repository URL (e.g., https://github.com/myorg/myrepo): ")
    target_file = input("Enter the file path to search for secrets (e.g., config/.env): ")
    
    files = fetch_repo_files(repo_url)
    
    if not files:
        print("No files found or failed to fetch files.")
        return

    file_urls = [file['download_url'] for file in files if file['path'] == target_file]

    if not file_urls:
        print(f"No target file '{target_file}' found in repository.")
        return

    # Search for secrets in the target file
    for file_url in file_urls:
        secrets_found = search_for_secrets(file_url, SECRET_KEYWORDS)
        for keyword, secrets in secrets_found.items():
            for secret in secrets:
                print(f"Found {keyword}: {secret}")
                exploit_secret(secret, keyword)

if __name__ == '__main__':
    main()
