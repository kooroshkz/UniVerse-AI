import time
import requests
import csv
import os
from bs4 import BeautifulSoup

BASE_URL = "https://www.universiteitleiden.nl"
STAFF_LIST_URL = f"{BASE_URL}/en/science/computer-science/staff#tab-6"
OUTPUT_FILE = "staff_info.csv"

def fetch_html(url):
    """Fetch the HTML content of a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_staff_list(html):
    """Parse the staff list page to extract staff profile links."""
    soup = BeautifulSoup(html, "html.parser")
    staff_links = []
    for link in soup.select(".table-list a"):
        href = link.get("href")
        if href and href.startswith("/en/staffmembers"):
            staff_links.append(BASE_URL + href)
    return staff_links

def parse_profile(html):
    """Parse the profile page to extract details."""
    soup = BeautifulSoup(html, "html.parser")
    name = soup.select_one("section.basics h1").text.strip()
    role = soup.select_one("section.basics p.context").text.strip()
    email = soup.select_one("a[href^='mailto:']")
    email = email.text.strip() if email else None
    phone = soup.select_one("a[href^='tel:']")
    phone = phone.text.strip() if phone else None
    address_section = soup.select_one("section.tab .role .col address")
    address = " ".join(address_section.stripped_strings) if address_section else None
    tags = [tag.text.strip() for tag in soup.select(".tags li a")]

    return {
        "Name": name,
        "Role": role,
        "Email": email,
        "Phone": phone,
        "Address": address,
        "Tags": ", ".join(tags)
    }

def save_to_csv(data, file_name):
    """Save staff details to a CSV file."""
    file_exists = os.path.exists(file_name)
    with open(file_name, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def scrape_staff_profiles():
    """Main function to scrape the staff profiles."""
    html = fetch_html(STAFF_LIST_URL)
    if not html:
        print("Failed to fetch the staff list.")
        return

    staff_links = parse_staff_list(html)
    print(f"Found {len(staff_links)} staff profiles.")

    scraped_data = []
    for idx, link in enumerate(staff_links, start=1):
        print(f"Processing ({idx}/{len(staff_links)}): {link}")
        profile_html = fetch_html(link)
        if not profile_html:
            print("Skipping due to fetch error.")
            continue
        
        profile_data = parse_profile(profile_html)
        scraped_data.append(profile_data)
        save_to_csv([profile_data], OUTPUT_FILE)

        # Delay to mimic human behavior and avoid IP ban
        time.sleep(2)
    
    print(f"Scraping completed. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_staff_profiles()