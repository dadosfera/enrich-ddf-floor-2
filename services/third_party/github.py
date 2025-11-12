"""
GitHub API Integration for Developer Profile Enrichment
Free tier: 5,000 requests/hour
"""

import logging
from typing import Any, Dict

import requests


logger = logging.getLogger(__name__)


class GitHubService:
    """GitHub API service for developer profile and company enrichment."""

    def __init__(self):
        from config import settings

        self.token = settings.github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Enrich-DDF-Floor-2/1.0",
        }

        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        else:
            logger.warning(
                "GitHub token not found. Set GITHUB_TOKEN environment variable for higher rate limits."
            )

    def enrich_developer_profile(self, username: str) -> Dict[str, Any]:
        """Enrich developer profile using GitHub API."""
        if not username:
            return {"success": False, "error": "Username is required"}

        try:
            # Get user profile
            user_response = requests.get(
                f"{self.base_url}/users/{username}", headers=self.headers, timeout=10
            )
            user_response.raise_for_status()
            user_data = user_response.json()

            # Get user repositories (top 10 by stars)
            repos_response = requests.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self.headers,
                params={"sort": "updated", "per_page": 10},
                timeout=10,
            )
            repos_response.raise_for_status()
            repos_data = repos_response.json()

            # Get user organizations
            orgs_response = requests.get(
                f"{self.base_url}/users/{username}/orgs",
                headers=self.headers,
                timeout=10,
            )
            orgs_response.raise_for_status()
            orgs_data = orgs_response.json()

            # Extract programming languages from repositories
            languages = set()
            for repo in repos_data:
                if repo.get("language"):
                    languages.add(repo["language"])

            return {
                "success": True,
                "profile": {
                    "username": user_data.get("login"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "bio": user_data.get("bio"),
                    "company": user_data.get("company"),
                    "location": user_data.get("location"),
                    "blog": user_data.get("blog"),
                    "twitter_username": user_data.get("twitter_username"),
                    "public_repos": user_data.get("public_repos", 0),
                    "followers": user_data.get("followers", 0),
                    "following": user_data.get("following", 0),
                    "created_at": user_data.get("created_at"),
                    "updated_at": user_data.get("updated_at"),
                },
                "repositories": [
                    {
                        "name": repo.get("name"),
                        "description": repo.get("description"),
                        "language": repo.get("language"),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "url": repo.get("html_url"),
                        "updated_at": repo.get("updated_at"),
                    }
                    for repo in repos_data[:5]  # Top 5 repositories
                ],
                "organizations": [
                    {
                        "login": org.get("login"),
                        "description": org.get("description"),
                        "url": org.get("html_url"),
                    }
                    for org in orgs_data
                ],
                "programming_languages": list(languages),
                "github_url": f"https://github.com/{username}",
            }

        except Exception as e:
            logger.error(f"GitHub API error for user {username}: {e}")
            return {"success": False, "error": str(e)}

    def enrich_organization(self, org_name: str) -> Dict[str, Any]:
        """Enrich organization/company data using GitHub API."""
        if not org_name:
            return {"success": False, "error": "Organization name is required"}

        try:
            # Get organization profile
            org_response = requests.get(
                f"{self.base_url}/orgs/{org_name}", headers=self.headers, timeout=10
            )
            org_response.raise_for_status()
            org_data = org_response.json()

            # Get organization repositories (top 10 by stars)
            repos_response = requests.get(
                f"{self.base_url}/orgs/{org_name}/repos",
                headers=self.headers,
                params={"sort": "stars", "per_page": 10},
                timeout=10,
            )
            repos_response.raise_for_status()
            repos_data = repos_response.json()

            # Get organization members (public members only)
            members_response = requests.get(
                f"{self.base_url}/orgs/{org_name}/members",
                headers=self.headers,
                params={"per_page": 20},
                timeout=10,
            )
            members_response.raise_for_status()
            members_data = members_response.json()

            # Extract tech stack from repositories
            tech_stack = set()
            for repo in repos_data:
                if repo.get("language"):
                    tech_stack.add(repo["language"])

            return {
                "success": True,
                "organization": {
                    "login": org_data.get("login"),
                    "name": org_data.get("name"),
                    "description": org_data.get("description"),
                    "email": org_data.get("email"),
                    "blog": org_data.get("blog"),
                    "location": org_data.get("location"),
                    "twitter_username": org_data.get("twitter_username"),
                    "public_repos": org_data.get("public_repos", 0),
                    "followers": org_data.get("followers", 0),
                    "following": org_data.get("following", 0),
                    "created_at": org_data.get("created_at"),
                    "updated_at": org_data.get("updated_at"),
                    "company_type": org_data.get("type"),
                },
                "repositories": [
                    {
                        "name": repo.get("name"),
                        "description": repo.get("description"),
                        "language": repo.get("language"),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "url": repo.get("html_url"),
                        "updated_at": repo.get("updated_at"),
                    }
                    for repo in repos_data[:5]  # Top 5 repositories
                ],
                "members": [
                    {
                        "login": member.get("login"),
                        "url": member.get("html_url"),
                        "type": member.get("type"),
                    }
                    for member in members_data[:10]  # Top 10 public members
                ],
                "tech_stack": list(tech_stack),
                "github_url": f"https://github.com/{org_name}",
            }

        except Exception as e:
            logger.error(f"GitHub API error for organization {org_name}: {e}")
            return {"success": False, "error": str(e)}

    def search_users_by_email(self, email: str) -> Dict[str, Any]:
        """Search for GitHub users by email (limited functionality)."""
        if not email:
            return {"success": False, "error": "Email is required"}

        try:
            # GitHub doesn't allow direct email search, but we can try to find users
            # by searching for commits with that email
            search_response = requests.get(
                f"{self.base_url}/search/commits",
                headers=self.headers,
                params={"q": f"author-email:{email}", "per_page": 5},
                timeout=10,
            )
            search_response.raise_for_status()
            search_data = search_response.json()

            users = []
            seen_users = set()

            for commit in search_data.get("items", []):
                author = commit.get("author", {})
                if author and author.get("login") not in seen_users:
                    seen_users.add(author.get("login"))
                    users.append(
                        {
                            "username": author.get("login"),
                            "name": author.get("name"),
                            "url": author.get("html_url"),
                            "avatar_url": author.get("avatar_url"),
                        }
                    )

            return {
                "success": True,
                "users": users,
                "total_count": len(users),
            }

        except Exception as e:
            logger.error(f"GitHub search error for email {email}: {e}")
            return {"success": False, "error": str(e)}

    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get current rate limit information."""
        try:
            response = requests.get(
                f"{self.base_url}/rate_limit", headers=self.headers, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"GitHub rate limit check error: {e}")
            return {"error": str(e)}
