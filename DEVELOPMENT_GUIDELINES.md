**DEVELOPMENT GUIDELINES**

1.  **Project Setup (Using Poetry with src layout)**
    
    *   Create a new project with standard `src/` structure:  
        `poetry new your-project-name --src`
        
    *   Navigate into the project folder:  
        `cd your-project-name`
        
    *   Activate the virtual environment:  
        `poetry shell`
        
2.  **Install Dependencies**
    
    *   Add core libraries:  
         ```bash
    poetry add beautifulsoup4,requests,playwright

VERSION CONTROL
    ---------------
    
    *   Use Git. Commit often with clear messages.
        
    *   Ignore `.env/`, `__pycache__/`, and `.mypy_cache/`.
        
    *   Track your `pyproject.toml` and `poetry.lock`.


   How to run the scraper:

To scrape all three sources:  
```bash
poetry run python scraping/src/scraping/main.py --books true --models true --quotes true

To scrape only books: 
```bash 
poetry run python scraping/src/scraping/main.py --books true

To scrape only models:  
```bash
poetry run python scraping/src/scraping/main.py --models true

To scrape only quotes:  
```bash
poetry run python scraping/src/scraping/main.py --quotes true