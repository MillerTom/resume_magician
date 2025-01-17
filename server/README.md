## Scrapping 


Steps to get the server up and running:

- Install requirements.txt `pip install -r requirements.txt`
- Create `.env` file on `main/.env` see `main/.env.example` for the variables needed
- Create superuser `python manage.py createsuperuser`
- Collect static files for installed apps `python manage.py collectstatic`
- Run the django server `python manage.py runserver 127.0.0.1:8003`
- Visit api docs page `http://127.0.0.1:8003/api/docs/`
- Visit admin panel `http://127.0.0.1:8003/admin`, log in with user created when doing superuser step.


### TO DO

Items to do:
- Parse scrape results.
- Monitoring script (system script).
