# ResumeMagician

## Environment variables
Create `.env` inside `server/main`
Get environment variables from administrator and put it to `.env`

## Start Server
`python(3) setup.py`


## Run Scraping
cd `server/`

all scrape with scrapers
`python(3) manage.py scrape`

single scrape with special scraper

`python(3) manage.py scrape <scraper name>`
`python(3) manage.py scrape ZipRecruiter`

all scraper names:
- Indeed
- ZipRecruiter
- LinkedIn
- Dice

Debug scrape with vscode
 - F5 key down