# scripts/scrape_books.py
import re
import time
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from typing import List, Dict

BASE_URL = "https://books.toscrape.com/"
OUT_PATH = Path("data/books.csv")

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def fetch_html(client: httpx.Client, url: str, retries: int = 3, backoff: float = 1.0) -> BeautifulSoup:
    for attempt in range(1, retries + 1):
        try:
            r = client.get(url, timeout=20.0)
            r.raise_for_status()
            return BeautifulSoup(r.text, "lxml")
        except Exception as e:
            if attempt == retries:
                raise
            time.sleep(backoff * attempt)
    # fallback (nunca chega aqui)
    return BeautifulSoup("", "lxml")

def get_categories(client: httpx.Client) -> List[Dict[str, str]]:
    soup = fetch_html(client, BASE_URL)
    cats = []
    for a in soup.select(".side_categories ul li ul li a"):
        name = a.get_text(strip=True)
        href = a.get("href")
        url = urljoin(BASE_URL, href)
        cats.append({"name": name, "url": url})
    return cats

def parse_rating(star_el) -> int:
    # <p class="star-rating Three">...</p>
    if star_el is None:
        return 0
    for cls in star_el.get("class", []):
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return 0

def clean_price(price_text: str) -> float:
    # '£51.77' -> 51.77
    if not price_text:
        return 0.0
    num = re.sub(r"[^0-9.,]", "", price_text).replace(",", "")
    try:
        return float(num)
    except ValueError:
        return 0.0

def extract_availability(text: str) -> str:
    # Mantemos o texto original, mas pode-se extrair quantidade
    # e.g. "In stock (22)"
    return re.sub(r"\s+", " ", text).strip()

def harvest_category(client: httpx.Client, cat_name: str, cat_url: str) -> List[Dict]:
    books = []
    next_url = cat_url

    while next_url:
        soup = fetch_html(client, next_url)
        for pod in soup.select("article.product_pod"):
            # título
            a = pod.select_one("h3 a")
            title = a.get("title", "").strip()

            # preço
            price_text = pod.select_one(".price_color")
            price = clean_price(price_text.get_text(strip=True) if price_text else "")

            # rating
            rating = parse_rating(pod.select_one(".star-rating"))

            # disponibilidade
            avail_el = pod.select_one(".instock.availability")
            availability = extract_availability(avail_el.get_text()) if avail_el else ""

            # imagem (relativa -> absoluta)
            img = pod.select_one("img")
            img_src = img.get("src", "") if img else ""
            image_url = urljoin(next_url, img_src)

            # link do produto (relativo -> absoluto)
            prod_rel = a.get("href")
            product_url = urljoin(next_url, prod_rel)

            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "category": cat_name,
                "image_url": image_url,
                "product_url": product_url,
            })

        # paginação
        next_li = soup.select_one("li.next a")
        if next_li:
            next_href = next_li.get("href")
            next_url = urljoin(next_url, next_href)
            time.sleep(0.5)  # throttle educado
        else:
            next_url = None

    return books

def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_books: List[Dict] = []
    with httpx.Client(headers=HEADERS, follow_redirects=True) as client:
        categories = get_categories(client)
        # print(f"Categorias encontradas: {len(categories)}")
        for idx, cat in enumerate(categories, start=1):
            # print(f"[{idx}/{len(categories)}] {cat['name']}")
            books = harvest_category(client, cat["name"], cat["url"])
            all_books.extend(books)
            time.sleep(0.5)  # cortesia entre categorias

    # IDs determinísticos
    df = pd.DataFrame(all_books)
    if df.empty:
        raise RuntimeError("Scraper não retornou dados. Verifique conectividade e seletores.")
    df.insert(0, "id", range(1, len(df) + 1))

    # Ordena por id (já sequencial) só por garantia
    df = df.sort_values("id").reset_index(drop=True)

    # Persistência
    df.to_csv(OUT_PATH, index=False)
    print(f"OK: {len(df)} registros salvos em {OUT_PATH}")

if __name__ == "__main__":
    main()
