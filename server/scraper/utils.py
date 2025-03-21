from apify_client import ApifyClient
from datetime import datetime, timedelta
import pytz
import re

import logging
logger = logging.getLogger(__name__)

def get_datetime(day):
    now_utc = datetime.now(pytz.utc)
    actual_date = now_utc - timedelta(days=day)
    return actual_date

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

class CustomApifyClient:
    actor_id = ''
    
    def __init__(self, api_key, actor_id):
        self.client = ApifyClient(api_key)
        self.actor_id = actor_id

    def start_actor(self, payload):
        return self.client.actor(self.actor_id).start(run_input=payload, wait_for_finish=False)