
import os
import logging
from typing import List, Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError

# ── Configuration ──────────────────────────────────────────────────────────────
load_dotenv()

API_KEY: str      = os.getenv("API_KEY", "")
API_BASE_URL: str = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)

# ── Pydantic Models ─────────────────────────────────────────────────────────────
class Post(BaseModel):
    id: int
    userId: int
    title: str = Field(..., min_length=1)
    body: str


class PostsResponse(BaseModel):
    total: int
    posts: List[Post]
    source: str = "api"  # "api" | "mock"


# ── FastAPI App ─────────────────────────────────────────────────────────────────
app = FastAPI(title="Public-API Explorer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ── Helpers ─────────────────────────────────────────────────────────────────────
def _validate_posts(raw: list, limit: int) -> List[Post]:
    """Validate a list of raw dicts into Post objects, skipping invalid records."""
    validated: List[Post] = []
    for item in raw[:limit]:
        try:
            validated.append(Post(**item))
        except ValidationError as exc:
            log.warning("Skipping invalid post record: %s", exc)
    return validated


def _fetch_from_api(limit: int) -> tuple[List[Post], str]:
    """Try to fetch posts from the upstream API. Returns (posts, source)."""
    url = f"{API_BASE_URL}/posts"
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}

    try:
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
        raw: list = response.json()
        posts = _validate_posts(raw, limit)
        log.info("Fetched %d posts from upstream API.", len(posts))
        return posts, "api"

    except requests.exceptions.Timeout:
        log.warning("Request to upstream timed out — falling back to mock data.")
    except requests.exceptions.ConnectionError as exc:
        log.warning("Connection error (%s) — falling back to mock data.", exc)
    except requests.exceptions.HTTPError as exc:
        log.warning("HTTP error from upstream (%s) — falling back to mock data.", exc)

    log.info("Serving %d mock posts.", len(posts))
    return posts, "mock"


# ── Routes ───────────────────────────────────────────────────────────────────────
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "Public-API Explorer is running"}


@app.get("/api/posts", response_model=PostsResponse, tags=["posts"])
def get_posts(limit: Optional[int] = 100):
    """Return a list of posts, optionally capped by *limit*."""
    if limit is not None and (limit < 1 or limit > 200):
        raise HTTPException(status_code=400, detail="limit must be between 1 and 200.")

    cap = limit or 100
    posts, source = _fetch_from_api(cap)

    return PostsResponse(total=len(posts), posts=posts, source=source)
