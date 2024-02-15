"""News scraper script for stories api"""
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_html(url):
    """gets html from url"""

    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf_8")
    return html


def parse_stories_bs(domain_url: str, html):
    """parses story into suitable lists to use"""

    stories = []
    soup = BeautifulSoup(html, "html.parser")
    scrape_results = soup.select(
        "a.ssrcss-its5xf-PromoLink, a.ssrcss-1mrs5ns-PromoLink, a.gs-c-promo-heading"
        )

    for story in scrape_results:
        if not story.get_text() or not story.get('href'):
            scrape_results.remove(story)
            continue
        stories.append({
            "url": domain_url + story.get('href'),
            "title": story.get_text()
        })

    return stories

if __name__ == "__main__":
    bbc_url = "https://www.bbc.co.uk/news/entertainment_and_arts"
    bbc_html_doc = get_html(bbc_url)
