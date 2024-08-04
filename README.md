GitHub and AWS Secrets Detection Script

This script is designed to simulate the detection and exploitation of secrets (e.g., AWS credentials, GitHub tokens, API keys) found in files within a GitHub repository. It showcases basic techniques used in penetration testing and security assessments.
Features

    Fetches files from a GitHub repository.
    Searches for secrets in specified files using regex patterns.
    Simulates exploitation of found secrets (e.g., accessing S3 buckets, using GitHub tokens).
    Implements logging and error handling.

Prerequisites

Before running the script, ensure you have the following:

    Python 3.x: The script is compatible with Python 3.x.
    Required Python Libraries: The script uses several Python libraries that need to be installed.

Setup Instructions

    Clone the Repository

    If you have a repository URL, you can clone it using Git:

    bash

git clone https://github.com/your-repo-url.git
cd your-repo-directory

Install Required Libraries

Install the necessary Python libraries using pip. You can do this by running:

bash

pip install requests boto3 PyGithub

Configure Environment Variables

Set up the required environment variables for GitHub and AWS:

    GitHub Token: Set the GitHub token as an environment variable. This token is needed to access private repositories.

    bash

export GITHUB_TOKEN='your_github_token_here'

AWS Region (optional): If you need to use a region other than us-west-2, set the AWS region as an environment variable:

bash

    export AWS_REGION='your_aws_region_here'

Prepare Your Configuration

Update the script with the following details:

    REPO_URL: The URL of the GitHub repository you want to scan.
    TARGET_FILE_PATH: The path to the file within the repository where secrets are expected to be found.

The default values in the script are:

python

    REPO_URL = 'https://api.github.com/repos/myorg/myrepo'
    TARGET_FILE_PATH = 'config/.env'

    Update these values as needed based on your target repository and file path.

Expected Inputs

When you run the script, you will be prompted to enter:

    GitHub Repository URL: Provide the URL of the GitHub repository you want to scan. Example: https://api.github.com/repos/myorg/myrepo.
    File Path: Enter the path to the file where secrets are expected to be found. Example: config/.env.

Running the Script

Run the script from the command line:

bash

python secrets_detection_script.py

You will be prompted to enter the GitHub repository URL and the file path where secrets are expected to be found.
Configuration Details

    Secrets Detection: The script looks for the following keywords in the specified files: AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, GITHUB_TOKEN, and API_KEY.
    Bucket Name: Currently hardcoded as 'example-bucket'. Update this to use a dynamic approach if needed.
    Rate Limiting: The script handles GitHub API rate limits with retry logic.

Logging

The script uses Python’s logging module to log information, warnings, and errors. Logs will be printed to the console. Modify the logging configuration in the script to save logs to a file or adjust the logging level if needed.
Ethical Considerations

Disclaimer: This script is for educational purposes only. Unauthorized use of this script against systems you do not own or have explicit permission to test is illegal. Always conduct penetration testing within legal and ethical boundaries.
Troubleshooting

    Missing Dependencies: Ensure all required libraries are installed.
    Invalid Token or Credentials: Verify that the environment variables are correctly set and that your tokens or credentials are valid.

Contact

For further assistance or questions, you can contact:

    Author: T1
    Email: Tadash10@protonmail.com
