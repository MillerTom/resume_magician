from apify_client import ApifyClient
from datetime import datetime, timedelta
import pytz

def get_datetime(day):
    now_utc = datetime.now(pytz.utc)
    actual_date = now_utc - timedelta(days=day)
    return actual_date

class CustomApifyClient:
    actor_id = ''
    
    def __init__(self, api_key, actor_id):
        self.client = ApifyClient(api_key)
        self.actor_id = actor_id

    def start_actor(self, payload):
        return self.client.actor(self.actor_id).call(run_input=payload)