import json
import os
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

import instaloader
import requests
from dotenv import load_dotenv


@dataclass
class Config:
    instagram_username: str
    keywords: List[str]
    poll_seconds: int
    post_scan_limit: int
    state_db_path: str
    seed_with_latest: bool
    kakao_rest_api_key: str
    kakao_refresh_token: str


class StateStore:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_posts (
                post_id TEXT PRIMARY KEY,
                shortcode TEXT NOT NULL,
                matched INTEGER NOT NULL,
                checked_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def has_post(self, post_id: str) -> bool:
        cur = self.conn.execute(
            "SELECT 1 FROM processed_posts WHERE post_id = ? LIMIT 1", (post_id,)
        )
        return cur.fetchone() is not None

    def add_post(self, post_id: str, shortcode: str, matched: bool) -> None:
        self.conn.execute(
            """
            INSERT OR IGNORE INTO processed_posts(post_id, shortcode, matched, checked_at)
            VALUES(?, ?, ?, ?)
            """,
            (post_id, shortcode, 1 if matched else 0, datetime.utcnow().isoformat()),
        )
        self.conn.commit()

    def is_empty(self) -> bool:
        cur = self.conn.execute("SELECT COUNT(*) FROM processed_posts")
        return (cur.fetchone() or [0])[0] == 0


class InstagramMonitor:
    def __init__(self) -> None:
        self.loader = instaloader.Instaloader(quiet=True, download_pictures=False)

    def fetch_recent_posts(self, username: str, limit: int) -> List[Dict[str, str]]:
        profile = instaloader.Profile.from_username(self.loader.context, username)
        results: List[Dict[str, str]] = []

        for idx, post in enumerate(profile.get_posts()):
            if idx >= limit:
                break
            results.append(
                {
                    "post_id": str(post.mediaid),
                    "shortcode": post.shortcode,
                    "caption": post.caption or "",
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                }
            )

        return results


def load_config() -> Config:
    load_dotenv()

    username = os.getenv("INSTAGRAM_USERNAME", "").strip()
    if not username:
        raise ValueError("INSTAGRAM_USERNAME is required")

    keywords_raw = os.getenv("KEYWORDS", "오늘의 메뉴")
    keywords = [k.strip().lower() for k in keywords_raw.split(",") if k.strip()]
    if not keywords:
        raise ValueError("KEYWORDS must contain at least one keyword")

    rest_api_key = os.getenv("KAKAO_REST_API_KEY", "").strip()
    refresh_token = os.getenv("KAKAO_REFRESH_TOKEN", "").strip()
    if not rest_api_key or not refresh_token:
        raise ValueError("KAKAO_REST_API_KEY and KAKAO_REFRESH_TOKEN are required")

    return Config(
        instagram_username=username,
        keywords=keywords,
        poll_seconds=int(os.getenv("POLL_SECONDS", "300")),
        post_scan_limit=int(os.getenv("POST_SCAN_LIMIT", "6")),
        state_db_path=os.getenv("STATE_DB_PATH", "state.sqlite3"),
        seed_with_latest=os.getenv("SEED_WITH_LATEST", "true").lower() == "true",
        kakao_rest_api_key=rest_api_key,
        kakao_refresh_token=refresh_token,
    )


def contains_keyword(text: str, keywords: List[str]) -> bool:
    lowered = text.lower()
    return any(k in lowered for k in keywords)


def refresh_kakao_access_token(rest_api_key: str, refresh_token: str) -> str:
    resp = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "refresh_token",
            "client_id": rest_api_key,
            "refresh_token": refresh_token,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"Failed to refresh Kakao token: {data}")
    return token


def send_kakao_message(access_token: str, instagram_user: str, post_url: str, caption: str) -> None:
    preview = caption.strip().replace("\n", " ")
    if len(preview) > 90:
        preview = preview[:87] + "..."

    template_object = {
        "object_type": "text",
        "text": f"[인스타 새 메뉴 감지]\n@{instagram_user}\n{preview}",
        "link": {
            "web_url": post_url,
            "mobile_web_url": post_url,
        },
        "button_title": "게시물 보기",
    }

    resp = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers={"Authorization": f"Bearer {access_token}"},
        data={"template_object": json.dumps(template_object, ensure_ascii=False)},
        timeout=15,
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("result_code") != 0:
        raise RuntimeError(f"Kakao send failed: {body}")


def run_monitor() -> None:
    config = load_config()
    store = StateStore(config.state_db_path)
    monitor = InstagramMonitor()

    print("Monitoring started")
    print(f"Target account: @{config.instagram_username}")
    print(f"Keywords: {config.keywords}")
    print(f"Polling every {config.poll_seconds}s")

    while True:
        try:
            posts = monitor.fetch_recent_posts(
                username=config.instagram_username,
                limit=config.post_scan_limit,
            )

            if config.seed_with_latest and store.is_empty() and posts:
                for post in posts:
                    store.add_post(post["post_id"], post["shortcode"], matched=False)
                print("Seeded current posts. Waiting for new posts only.")
                time.sleep(config.poll_seconds)
                continue

            for post in reversed(posts):
                if store.has_post(post["post_id"]):
                    continue

                matched = contains_keyword(post["caption"], config.keywords)
                store.add_post(post["post_id"], post["shortcode"], matched=matched)

                if matched:
                    token = refresh_kakao_access_token(
                        config.kakao_rest_api_key,
                        config.kakao_refresh_token,
                    )
                    send_kakao_message(
                        access_token=token,
                        instagram_user=config.instagram_username,
                        post_url=post["url"],
                        caption=post["caption"],
                    )
                    print(f"Alert sent: {post['url']}")
                else:
                    print(f"New post skipped (keyword not matched): {post['url']}")

        except Exception as exc:
            print(f"[ERROR] {exc}")

        time.sleep(config.poll_seconds)


if __name__ == "__main__":
    run_monitor()
