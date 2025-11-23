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
    return [{"id": repo.id, "name": repo.name} for repo in repos]
