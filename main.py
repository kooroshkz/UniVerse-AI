import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re  # Importing the regular expression module

# Set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
base_url = "https://www.universiteitleiden.nl/en/academic-staff/overview?pageNumber="


# Function to scrape data from a single page
def scrape_page(page_num):
    url = f"{base_url}{page_num}"
    driver.get(url)

    # Wait for the content div to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    staff_data = []

    # Find the main content div and then the ul within it
    content_div = soup.find("div", id="content")
    if not content_div:
        return None

    staff_list = content_div.find("ul")
    if not staff_list:
        return None

    for staff in staff_list.find_all("li"):
        # Extract the profile link
        link_tag = staff.find("a", href=True)
        if not link_tag:
            continue  # Skip if no profile link is found
        profile_url = f"https://www.universiteitleiden.nl{link_tag['href']}"

        # Extract name, title, and affiliations
        name_div = staff.find("div", class_="has-edit-button")
        if name_div:
            name = name_div.find("strong").text.strip() if name_div.find("strong") else "N/A"
            title = name_div.find("p").text.strip().replace("\n", " ").strip() if name_div.find("p") else "N/A"
            # Clean up title: remove spaces between title and name
            title = re.sub(r'\s+', ' ', title)  # Replaces multiple spaces with a single space
            title = title.strip()  # Trim any leading/trailing spaces
            affiliations = [aff.text.strip().replace("\n", " ").strip() for aff in name_div.find_all("li")]

            # Append to the list
            staff_data.append({
                "name": name,
                "title": title,
                "affiliations": ", ".join(affiliations),  # Join affiliations in a single string
                "profile_url": profile_url
            })

    return staff_data


# Function to scrape individual profile page and return data
def scrape_profile_page(profile_url):
    driver.get(profile_url)

    # Wait for the basics section to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "basics")))

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the "facts" dl element (for name, telephone, email, ORCID)
    facts_dl = soup.find("dl", class_="facts search-off")
    if not facts_dl:
        return None  # If no facts section, skip this profile

    profile_data = {}

    # Extract name (if available)
    name_dt = facts_dl.find("dt", string="Name")
    if name_dt:
        name_dd = name_dt.find_next_sibling("dd")
        profile_data["name"] = name_dd.text.strip() if name_dd else "N/A"

    # Extract telephone (if available)
    phone_dt = facts_dl.find("dt", string="Telephone")
    if phone_dt:
        phone_dd = phone_dt.find_next_sibling("dd")
        phone = phone_dd.find("a")["href"] if phone_dd else "N/A"
        profile_data["telephone"] = phone.replace("tel:", "")  # Clean up the tel: part

    # Extract email (if available)
    email_dt = facts_dl.find("dt", string="E-mail")
    if email_dt:
        email_dd = email_dt.find_next_sibling("dd")
        email = email_dd.find("a")["href"] if email_dd else "N/A"
        profile_data["email"] = email.replace("mailto:", "")  # Clean up the mailto: part

    # Extract ORCID (if available)
    orcid_dt = facts_dl.find("dt", string="ORCID iD")
    if orcid_dt:
        orcid_dd = orcid_dt.find_next_sibling("dd")
        orcid = orcid_dd.find("a")["href"] if orcid_dd else "N/A"
        profile_data["orcid"] = orcid

    # Extract work address from the "Contact" section (with id="work-address")
    work_address_header = soup.find("h3", id="work-address")
    if work_address_header:
        address = work_address_header.find_next("address")
        if address:
            # Clean the address by removing spaces, line breaks, and non-breaking spaces (nbsp)
            cleaned_address = ' '.join(address.stripped_strings).replace('\n', ' ').replace('&nbsp;', ' ').strip()
            profile_data["work_address"] = cleaned_address
        else:
            profile_data["work_address"] = "N/A"
    else:
        profile_data["work_address"] = "N/A"

    return profile_data


# Scrape the list of staff and their profile URLs
all_staff_data = []
page = 1
while True:
    print(f"Scraping page {page}")
    page_data = scrape_page(page)
    if not page_data:  # Stop if no data found on the page
        print("No more staff data found; stopping scraper.")
        break
    all_staff_data.extend(page_data)
    page += 1
    time.sleep(1)  # Delay to avoid overloading the server

# Convert the list of staff data to a DataFrame
df = pd.DataFrame(all_staff_data)

# Scrape additional information for each profile
for index, row in df.iterrows():
    print(f"Scraping profile: {row['profile_url']}")
    profile_data = scrape_profile_page(row['profile_url'])
    if profile_data:
        # Add the scraped details as new columns in the existing DataFrame
        df.at[index, "telephone"] = profile_data.get("telephone", "N/A")
        df.at[index, "email"] = profile_data.get("email", "N/A")
        df.at[index, "orcid"] = profile_data.get("orcid", "N/A")
        df.at[index, "work_address"] = profile_data.get("work_address", "N/A")
    time.sleep(1)  # Delay to avoid overloading the server

# Close the driver
driver.quit()

# Save the final DataFrame to a CSV file
df.to_csv("staff_data.csv", index=False)