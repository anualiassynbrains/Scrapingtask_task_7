import argparse
import asyncio
from scrapers.scraper import Scraping


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