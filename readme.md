# ApplyJobForever

## Environment variables
Create `.env` inside `server/main`
Get environment variables from administrator and put it to `.env`

## Start Server
`python3 setup.py`

## Setup Scraper Environments
### Create Superuser
`python3 manage.py createsuperuser`

### Go to admin page and login with your credetial.
`http://localhost:5000/admin`

### Add Scrapers and Configurations
Go to `Scraper` and `Configuration` pages and add scrapers and configurations.

## Test Scrapers
`python3 manage.py test`