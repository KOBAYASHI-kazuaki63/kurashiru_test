import json
from utils.ScrapeWLLM import ScrapeWLLM

urls = [
    "https://www.kurashiru.com/recipes/e3fd1786-3931-4324-81a6-1f1f5b02ed55",
    "https://www.kurashiru.com/recipes/34a5fc6a-8411-47a3-82ad-555332eb9671",
    "https://www.kurashiru.com/recipes/287235e4-db7e-4e4c-b0a3-0008581de012",
]

if __name__ == "__main__":
    scraper = ScrapeWLLM(urls)
    result = scraper.scrape()
    with open("result/output.json", "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
