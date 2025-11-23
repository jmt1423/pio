from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from ..services.ghService import GithubService

router = APIRouter(prefix="/github", tags=["github"])

try:
    github_service = GithubService()
except Exception as e:
    print(f"Error initializing GithubService: {str(e)}")


@router.get("/repos")
async def get_all_repos() -> List[Dict[str, Any]]:
    if not github_service:
        raise HTTPException(status_code=500, detail="GithubService not initialized")
    repos = github_service.get_user_repos()
    return [
        {"id": repo.id, "name": repo.name, "full_name": repo.full_name}
        for repo in repos
    ]


@router.get("/repo/{owner}/{repo_name}")
async def get_repo_by_name(owner: str, repo_name: str) -> Dict[str, Any]:
    if not github_service:
        raise HTTPException(status_code=500, detail="GithubService not initialized")

    repo = github_service.get_repo(f"{owner}/{repo_name}")

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    issues = repo.get_issues(state="all")
    pulls = repo.get_pulls(state="all")

    issues_list = [
        {
            "id": issue.id,
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "labels": [label.name for label in issue.labels],
        }
        for issue in issues
    ]

    pulls_list = [
        {
            "id": pull.id,
            "number": pull.number,
            "title": pull.title,
            "state": pull.state,
        }
        for pull in pulls
    ]

    return {
        "id": repo.id,
        "name": repo.name,
        "issues": issues_list,
        "pulls": pulls_list,
    }
