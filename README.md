Scraping Project - Books, Models, and Quotes

This project scrapes data from three websites:

1.  Books from [https://books.toscrape.com](https://books.toscrape.com)
    
2.  Models from [https://huggingface.co/models](https://huggingface.co/models)
    
3.  Quotes from [https://quotes.toscrape.com/scroll](https://quotes.toscrape.com/scroll)

SETUP INSTRUCTIONS (USING POETRY)
---------------------------------

1.  **Install Poetry**  
    Follow the instructions at:  
    [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)
    
2.  Clone the repository  git clone https://github.com/anualiassynbrains/scrapingtask_task_7
    ```bash
    cd your-repo-name
    
3.  Install project dependencies
    ```bash
    poetry add beautifulsoup4,requests,playwright
    
5.  Activate virtual environment
    ```bash
      poetry shell
    
How to run the scraper:

To scrape all three sources:  
```bash
poetry run python scraping/src/scraping/main.py --books true --models true --quotes true
```
To scrape only books: 
```bash 
poetry run python scraping/src/scraping/main.py --books true
```
To scrape only models:  
```bash
poetry run python scraping/src/scraping/main.py --models true
```
To scrape only quotes:  
```bash
poetry run python scraping/src/scraping/main.py --quotes true
```
Scraped data is saved in:

*   staticwebscrape.json (for books)
    
*   huggingface\_models.json (for models)
    
*   quotes.json (for quotes)
    

All files are saved in the "scraping/src/scraping/output" folder.

Make sure you have internet while running the scraper.

Run "playwright install" once before using Playwright for the first time.
