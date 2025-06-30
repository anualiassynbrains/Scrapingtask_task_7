import argparse
from bs4 import BeautifulSoup
import requests
import asyncio
import re
import json
from playwright.async_api import async_playwright

class Scraping:
    def __init__(self,books,model,quotes):
        self.books=books
        self.model=model
        self.quotes=quotes
        self.rating_dict={1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five'}
        


    def find_details(self,litext): 
        
        divv=litext.find('h3').find('a')
        title=divv['title']
        url=divv['href']
        price=litext.find('p',class_='price_color')
        rating_word=litext.find('p',class_='star-rating')
        for key,value in self.rating_dict.items():
                if value==rating_word['class'][1]:
                        rating_number=key
        
        price_text = price.get_text(strip=True)
        price = float(price_text.replace('£', ''))
        output={
        "model_name":title ,
        "price": price,
        "rating": rating_number,
        "source_url": url,
        "data_source": "bookstoscrape"
        }
        return output


    def get_books(self):
        r=requests.get('https://books.toscrape.com/')
        soup = BeautifulSoup(r.content, 'html.parser')
        whole_books=[]
        div_text=soup.find_all('article',class_='product_pod')

        for litext in div_text:
                out=self.find_details(litext)
                whole_books.append(out)
        with open(r'C:\Users\hp\Documents\synbrains_trainee_works\scrapingwork\scraping\src\scraping\output\staticwebscrape.json', 'w', encoding='utf-8') as file:
                json.dump(whole_books, file, indent=4, ensure_ascii=False)


    async def scrape_models(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://huggingface.co/models")

            model_cards = []
            seen = set()

            while len(model_cards) < 30:
                await page.mouse.wheel(0, 5000)  
                await page.wait_for_timeout(1500)  

                cards = await page.query_selector_all("article[class*='overview-card-wrapper']")

                for card in cards:
                    try:
                        
                        name_tag = await card.query_selector("a[href^='/']")
                        source_url = await name_tag.get_attribute("href")

                       
                        model_name_elem = await card.query_selector("h4")
                        model_name = await model_name_elem.inner_text() if model_name_elem else source_url.strip("/")

                        if model_name in seen:
                            continue
                        seen.add(model_name)

                       
                        full_text = await card.inner_text()
                        numbers = re.findall(r"\b[\d,]+(?:\.\d+)?\b", full_text)

                        
                        downloads = numbers[0] if len(numbers) > 0 else "0"
                        likes = numbers[-1] if len(numbers) > 1 else "0"

                        
                        downloads = downloads.replace(",", "")
                        likes = likes.replace(",", "")

                        model_cards.append({
                            "model_name": model_name,
                            "likes": int(likes),
                            "downloads": downloads,
                            "source_url": source_url,
                            "data_source": "huggingface"
                        })

                        if len(model_cards) >= 30:
                            break
                    except Exception as e:
                        continue

            await browser.close()

            with open(r"C:\Users\hp\Documents\synbrains_trainee_works\scrapingwork\scraping\src\scraping\output\huggingface_models.json", "w", encoding="utf-8") as f:
                json.dump(model_cards, f, indent=4, ensure_ascii=False)

            

    async def scrape_quotes(self):
     quotes=[]
     async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        async def handle_response(response):
            if "api/quotes?page=" in response.url and response.status == 200:
                print(response.url)
                data = await response.json()
                for item in data['quotes']:
                    quote = {
                        "quote_text": item['text'],
                        "author_name": item['author']['name'],
                        "tags": item['tags'],
                        "data_source": "quotestoscrape"
                    }
                    quotes.append(quote)

        page.on("response", handle_response)

        await page.goto("https://quotes.toscrape.com/scroll")

        
       
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await asyncio.sleep(2)  
        

        await browser.close()

    
        with open(r'C:\Users\hp\Documents\synbrains_trainee_works\scrapingwork\scraping\src\scraping\output\quotes.json', "w", encoding="utf-8") as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)     

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--books', type=str, default='false')
    parser.add_argument('--models', type=str, default='false')
    parser.add_argument('--quotes', type=str, default='false')
    args = parser.parse_args()

    def to_bool(val): return val.lower() == "true"

    scraper = Scraping(
        books=to_bool(args.books),
        model=to_bool(args.models),
        quotes=to_bool(args.quotes)
    )

    if scraper.books:
        print(" Scraping books...")
        scraper.get_books()

    if scraper.model:
        print(" Scraping models...")
        await scraper.scrape_models()

    if scraper.quotes:
        print(" Scraping quotes...")
        await scraper.scrape_quotes()

if __name__ == "__main__":
    asyncio.run(main())