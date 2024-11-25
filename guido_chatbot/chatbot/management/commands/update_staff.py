from django.core.management.base import BaseCommand
from chatbot.utils import update_staff_data_from_csv
import os
import subprocess

class Command(BaseCommand):
    help = "Update staff data from scraper"

    def handle(self, *args, **kwargs):
        # Path to the scraper
        scraper_path = os.path.join("guido_chatbot", "chatbot", "scraper.py")

        # Run the scraper
        subprocess.run(["python", scraper_path], check=True)

        # Update the database
        csv_file_path = os.path.join("guido_chatbot", "chatbot", "complete_staff_info.csv")
        update_staff_data_from_csv(csv_file_path)
        self.stdout.write("Staff data updated successfully.")
