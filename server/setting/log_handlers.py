import logging
from django.apps import apps

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        try:
            LogEntry = apps.get_model('setting', 'LogEntry')
            log_entry = LogEntry(
                message=self.format(record),
                severity=record.levelname,
                source=record.name,
            )
            log_entry.save()
        except Exception:
            pass
