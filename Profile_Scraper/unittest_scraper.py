from unittest.mock import patch, mock_open, MagicMock
import requests
import os
from bs4 import BeautifulSoup
from Scraper import fetch_html, parse_staff_list, parse_profile, save_to_csv

def test_fetch_html_success():
    """Fetches the raw HTML content from a given URL."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        result = fetch_html("http://example.com")
        assert result == "<html></html>", "HTML content did not match the expected value."

def test_parse_staff_list():
    """Extracts a list of staff profile links from the staff listing page."""
    html = '''
    <html>
    <ul class="table-list">
        <li><a href="/en/staffmembers/joost-batenburg">Joost Batenburg</a></li>
        <li><a href="/en/staffmembers/frank-de-boer">Frank de Boer</a></li>
    </ul>
    </html>
    '''
    expected_links = [
        "https://www.universiteitleiden.nl/en/staffmembers/joost-batenburg",
        "https://www.universiteitleiden.nl/en/staffmembers/frank-de-boer",
    ]

    result = parse_staff_list(html)
    assert result == expected_links, "Staff links did not match the expected value."

def test_parse_profile():
    """Extracts detailed information about a staff member from their profile page."""
    html = '''
    <html>
    <section class="basics">
        <h1>John Doe</h1>
        <p class="context">Professor</p>
    </section>
    <a href="mailto:j.doe@example.com">j.doe@example.com</a>
    <a href="tel:+123456789">+123456789</a>
    <section class="tab">
        <div class="role">
            <div class="col">
                <address>123 Academic Way, Leiden</address>
            </div>
        </div>
    </section>
    <ul class="tags">
        <li><a>Research</a></li>
        <li><a>Teaching</a></li>
    </ul>
    </html>
    '''
    expected_profile = {
        "Name": "John Doe",
        "Role": "Professor",
        "Email": "j.doe@example.com",
        "Phone": "+123456789",
        "Address": "123 Academic Way, Leiden",
        "Tags": "Research, Teaching",
    }

    result = parse_profile(html)
    assert result == expected_profile, "Profile data did not match the expected value."

def test_save_to_csv_new_file():
    """Saves a list of dictionaries (staff data) to a CSV file."""
    with patch("builtins.open", new_callable=mock_open) as mock_open_file, patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        data = [
            {
                "Name": "John Doe",
                "Role": "Professor",
                "Email": "j.doe@example.com",
                "Phone": "+123456789",
                "Address": "123 Academic Way, Leiden",
                "Tags": "Research, Teaching",
            }
        ]

        save_to_csv(data, "test.csv")

        mock_open_file.assert_called_once_with("test.csv", "a", newline="", encoding="utf-8")
        handle = mock_open_file()
        handle.write.assert_called()

def test_save_to_csv_existing_file():
    """Tests saving data to an existing CSV file."""
    with patch("builtins.open", new_callable=mock_open) as mock_open_file, patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True
        data = [
            {
                "Name": "John Doe",
                "Role": "Professor",
                "Email": "j.doe@example.com",
                "Phone": "+123456789",
                "Address": "123 Academic Way, Leiden",
                "Tags": "Research, Teaching",
            }
        ]

        save_to_csv(data, "test.csv")

        mock_open_file.assert_called_once_with("test.csv", "a", newline="", encoding="utf-8")
        handle = mock_open_file()
        handle.write.assert_called()

if __name__ == "__main__":
    print("Running test_fetch_html_success...")
    test_fetch_html_success()

    print("Running test_parse_staff_list...")
    test_parse_staff_list()

    print("Running test_parse_profile...")
    test_parse_profile()

    print("Running test_save_to_csv_new_file...")
    test_save_to_csv_new_file()

    print("Running test_save_to_csv_existing_file...")
    test_save_to_csv_existing_file()

    print("All tests executed.")
