from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import clean_media


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_media, 'interval', seconds=5)
    scheduler.start()
