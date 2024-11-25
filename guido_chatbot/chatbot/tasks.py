from celery import shared_task
import os
from chatbot.utils import update_staff_data_from_csv

@shared_task
def run_scraper_and_update():
    scraper_path = os.path.join("guido_chatbot", "chatbot", "scraper.py")
    os.system(f"python {scraper_path}")
    csv_file_path = os.path.join("guido_chatbot", "chatbot", "complete_staff_info.csv")
    update_staff_data_from_csv(csv_file_path)

@shared_task
def add(x, y):
    return x + y