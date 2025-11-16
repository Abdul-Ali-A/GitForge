import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

#Load the clean version of GitHUb Access Token from the .env file.
def gh_token():
    token=os.getenv("GH_TOKEN").strip()
    if not token:
        raise Exception("Github Token not found!")
        exit(1)
    return token