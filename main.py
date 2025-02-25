from bs4 import BeautifulSoup
import requests

search=input("Enter Search Term: ")
params={"q":search}
r=requests.get("https://www.bing.com/search",params=params)

soup=BeautifulSoup(r.text,features="html.parser")

results=soup.find("ol",{"id":"b_results"})
links=results.findAll("li",{"class": "b_algo"})

for items in links:
    item_text=items.find("a").text
    item_href=items.find("a").attrs["href"]

    if item_text and item_href:
        print(item_text)
        print(item_href)
        print("Summary:", items.find("a").parent.parent.find("p").text)
        children=items.find("h2")
        print("Next sibling of the h2:",children.next_sibling)