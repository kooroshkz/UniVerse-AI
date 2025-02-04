import csv
from unittest.mock import patch, mock_open, MagicMock
import requests
import os
from bs4 import BeautifulSoup
from Scraper import fetch_html, parse_staff_list, parse_profile, save_to_csv

def test_fetch_html_real():
    """Test fetching real HTML content from the Leiden University website."""
    url = "https://www.universiteitleiden.nl/en/science/computer-science/staff#tab-6"
    html = fetch_html(url)
    assert html is not None, "Failed to fetch HTML content."
    assert "<html" in html.lower(), "Fetched content does not appear to be HTML."

def test_parse_staff_list_real():
    """Test parsing staff list links from the real staff page."""
    url = "https://www.universiteitleiden.nl/en/science/computer-science/staff#tab-6"
    html = fetch_html(url)
    staff_links = parse_staff_list(html)
    assert len(staff_links) > 0, "No staff links found."
    assert staff_links[0].startswith("https://www.universiteitleiden.nl/en/staffmembers"), "Staff links do not match the expected format."

def test_parse_profile_real():
    """Test parsing a real staff profile."""
    profile_url = "https://www.universiteitleiden.nl/en/staffmembers/joost-batenburg"
    html = fetch_html(profile_url)
    profile_data = parse_profile(html)
    assert "Name" in profile_data, "Profile data does not contain 'Name'."
    assert profile_data["Name"] == "Joost Batenburg", "Name does not match the expected value."
    assert "Role" in profile_data, "Profile data does not contain 'Role'."

def test_save_to_csv_real():
    """Test saving real data to a CSV file."""
    data = [
        {
            "Name": "Joost Batenburg",
            "Role": "Professor",
            "Email": "joost.batenburg@example.com",
            "Phone": "+31 71 527 7000",
            "Address": "123 Academic Way, Leiden",
            "Tags": "Research, Teaching",
        }
    ]
    test_file = "test_real.csv"
    save_to_csv(data, test_file)
    assert os.path.exists(test_file), "CSV file was not created."
    os.remove(test_file)  # Clean up after test

def test_save_to_csv_existing_file_real():
    """Test saving data to an existing CSV file using real file operations."""
    test_file = "test_existing.csv"

    # Initial data to create the file
    initial_data = [
        {
            "Name": "Alice Smith",
            "Role": "Assistant Professor",
            "Email": "alice.smith@example.com",
            "Phone": "+1234567890",
            "Address": "123 Academic Way, Leiden",
            "Tags": "Research",
        }
    ]

    # Data to append to the file
    additional_data = [
        {
            "Name": "Bob Jones",
            "Role": "Professor",
            "Email": "bob.jones@example.com",
            "Phone": "+0987654321",
            "Address": "456 Science Blvd, Leiden",
            "Tags": "Teaching, Research",
        }
    ]

    # Create the file with initial data
    save_to_csv(initial_data, test_file)

    # Append additional data
    save_to_csv(additional_data, test_file)

    # Read back the file to verify the contents
    with open(test_file, "r", encoding="utf-8") as csvfile:
        reader = list(csv.DictReader(csvfile))
        assert len(reader) == 2, "CSV file does not contain the expected number of rows."
        assert reader[0]["Name"] == "Alice Smith", "First row does not match the initial data."
        assert reader[1]["Name"] == "Bob Jones", "Second row does not match the appended data."

    # Clean up the test file
    os.remove(test_file)


if __name__ == "__main__":
    print("Running test_fetch_html_success...")
    test_fetch_html_real()

    print("Running test_parse_staff_list...")
    test_parse_staff_list_real()

    print("Running test_parse_profile...")
    test_parse_profile_real()

    print("Running test_save_to_csv_new_file...")
    test_save_to_csv_real()

    print("Running test_save_to_csv_existing_file...")
    test_save_to_csv_existing_file_real()

    print("All tests executed.")