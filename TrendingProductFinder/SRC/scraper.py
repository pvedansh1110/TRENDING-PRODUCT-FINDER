import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


def scrape_amazon(keyword):
    url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    products = []

    for item in soup.select("div.s-result-item"):
        title = item.select_one("span.a-text-normal")
        price = item.select_one("span.a-price-whole")

        if title and price:
            products.append({
                "title": title.text.strip(),
                "price": price.text.strip(),
                "source": "Amazon"
            })

    return products


def scrape_flipkart(keyword):
    url = f"https://www.flipkart.com/search?q={keyword.replace(' ', '+')}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    products = []

    for item in soup.select("div._1AtVbE"):
        title = item.select_one("div._4rR01T")
        price = item.select_one("div._30jeq3")

        if title and price:
            products.append({
                "title": title.text.strip(),
                "price": price.text.strip(),
                "source": "Flipkart"
            })

    return products


def get_trending_products(keyword):
    amazon_data = scrape_amazon(keyword)
    flipkart_data = scrape_flipkart(keyword)

    return amazon_data + flipkart_data
