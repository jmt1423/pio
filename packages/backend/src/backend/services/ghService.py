import os
from typing import List, Optional

from dotenv import load_dotenv
from github import Github
from github.Repository import Repository

load_dotenv()


class GithubService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is not set")

        self.client = Github(self.token)

    def get_user_repos(self, username: Optional[str] = None) -> List[Repository]:
        try:
            if username:
                user = self.client.get_user(username)
                return list(user.get_repos())
            else:
                return list(self.client.get_user().get_repos())
        except Exception as e:
            print(f"Error fetching user repos: {e}")
            return []

    def get_repo(self, repo_name: str):
        try:
            return self.client.get_repo(repo_name)
        except Exception as e:
            print(f"Error fetching repo: {e}")
            return None

    def get_pull_request(self, repo_name: str, pull_number: int):
        try:
            repo = self.get_repo(repo_name)
            if repo:
                return repo.get_pull(pull_number)
        except Exception as e:
            print(f"Error fetching pull request: {e}")
            return None
