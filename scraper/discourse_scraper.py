import requests
from bs4 import BeautifulSoup


def scrape_discourse(url: str, start_date: str, end_date: str):
    """Scrape posts from Discourse forum within date range"""
    posts = []
    page = 1

    while True:
        response = requests.get(f"{url}.json?page={page}")
        data = response.json()

        if not data.get("post_stream", {}).get("posts"):
            break

        for post in data["post_stream"]["posts"]:
            if start_date <= post["created_at"] <= end_date:
                posts.append({
                    "id": post["id"],
                    "content": BeautifulSoup(post["cooked"], "html.parser").get_text()
                })

        page += 1

    return posts

posts = scrape_discourse(
    "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34",
    "2025-01-01",
    "2025-04-14"
)
print(posts[:2])  # Sample output