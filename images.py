from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import os

def start_search():
    search = input("Search for: ")
    params = {"q": search, "form": "HDRSC2"}  
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
    }
    dir_name = search.replace(" ", "_").lower()
    os.makedirs(dir_name, exist_ok=True)
    response = requests.get("https://www.bing.com/images/search", params=params, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch images from Bing.")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")
    count = 0
    for img in images:
        img_url = img.get("src") or img.get("data-src")  
        if img_url and img_url.startswith("http"):
            try:
                img_response = requests.get(img_url, headers=headers, timeout=5)
                img_response.raise_for_status()
                img_obj = Image.open(BytesIO(img_response.content))
                img_format = img_obj.format if img_obj.format else "JPEG"
                filename = os.path.join(dir_name, f"image_{count}.{img_format.lower()}")

                img_obj.save(filename, img_format)
                print(f"Saved: {filename}")
                count += 1

            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

    print("Image scraping completed.")

start_search()
