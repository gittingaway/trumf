import requests
from bs4 import BeautifulSoup


def get_headers():
    return {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }


## categories = name, popularity, points


def get_deals(hits: int, page: int, category: str = "name"):
    url = f"https://trumfnetthandel.no/category/paged/all/{hits}/{page}/{category}"
    headers = get_headers()
    response = requests.request("GET", url, headers=headers, verify=False)
    return response.text


def extract_merchant_data(html):
    soup = BeautifulSoup(html, "html.parser")
    merchants = []

    for merchant_tile in soup.find_all("a", class_="merchant-tile"):
        merchant = {
            "name": merchant_tile.get("data-name"),
            "image_url": (
                merchant_tile.find("img", class_="merchant-image").get("src")
                if merchant_tile.find("img", class_="merchant-image")
                else None
            ),
            "cashback": merchant_tile.get("data-percentage"),
            "cashback_path": merchant_tile.get("href"),
        }
        merchants.append(merchant)

    return merchants


def main():
    merchants = []
    index = 0
    while True:
        deals = get_deals(15, index)
        if not deals:
            break
        merchants += extract_merchant_data(deals)
        index += 1
    print(merchants)


if __name__ == "__main__":
    main()
