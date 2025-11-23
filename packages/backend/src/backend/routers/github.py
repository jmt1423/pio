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


@router.get("/repo/{owner}/{repo_name}/pull/{pull_number}")
async def get_pull_request(
    owner: str, repo_name: str, pull_number: int
) -> Dict[str, Any]:
    if not github_service:
        raise HTTPException(status_code=500, detail="GithubService not initialized")

    repo = github_service.get_repo(f"{owner}/{repo_name}")

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    pull_request = github_service.get_pull_request(f"{owner}/{repo_name}", pull_number)

    if not pull_request:
        raise HTTPException(status_code=404, detail="Pull request not found")

    files = pull_request.get_files()

    files_data = []

    for file in files:
        file_info = {
            "filename": file.filename,
            "status": file.status,
            "additions": file.additions,
            "deletions": file.deletions,
            "changes": file.changes,
            "patch": file.patch,
            "blob_url": file.blob_url,
            "raw_url": file.raw_url if hasattr(file, "raw_url") else None,
        }

        files_data.append(file_info)

    return {
        "id": pull_request.id,
        "number": pull_request.number,
        "title": pull_request.title,
        "state": pull_request.state,
        "body": pull_request.body,
        "created_at": pull_request.created_at.isoformat()
        if pull_request.created_at
        else None,
        "updated_at": pull_request.updated_at.isoformat()
        if pull_request.updated_at
        else None,
        "closed_at": pull_request.closed_at.isoformat()
        if pull_request.closed_at
        else None,
        "merged_at": pull_request.merged_at.isoformat()
        if pull_request.merged_at
        else None,
        "base": {
            "ref": pull_request.base.ref,
            "sha": pull_request.base.sha,
            "repo_name": pull_request.base.repo.full_name,
        },
        "head": {
            "ref": pull_request.head.ref,
            "sha": pull_request.head.sha,
            "repo_name": pull_request.head.repo.full_name,
        },
        "files": files_data,
        "total_additions": pull_request.additions,
        "total_deletions": pull_request.deletions,
        "changed_files": pull_request.changed_files,
    }
