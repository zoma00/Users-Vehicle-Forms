from datetime import datetime
import logging

class TimezoneFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=pytz.timezone('Asia/Kolkata'))  # Replace with your desired timezone
        return dt.strftime(datefmt or '%Y-%m-%d %H:%M:%S %z')
