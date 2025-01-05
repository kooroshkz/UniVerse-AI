# UniVerse AI: Leiden University Students Assistant Bot
### Group no.11 - Software Development (2024-2025)

## Project Overview
UniVerse AI is a comprehensive platform designed to streamline access to university-related information. It provides a user-friendly interface for querying academic schedules, staff details, and campus facilities. Built using Django, the platform integrates advanced NLP via OpenAI API and employs tools like SQLite3, Celery, and BeautifulSoup for efficient data handling and dynamic updates.

---

## Team Members and Roles
- **Diego Canas Jimenez** (s3856216): Database Engineer
  - Responsible for designing and managing the SQLite3 database structure.
  - Implemented data integration pipelines for seamless database updates.
- **Koorosh Komeili Zadeh** (s3893995): DevOps Engineer
  - Set up and maintained the development environment and deployment pipeline.
  - Configured Celery for automated scraping and database updates.
- **Emmanouil Zagoritis** (s4076893): Backend Developer
  - Developed the Django backend, including API integrations and chatbot functionality.
  - Created and managed database models and views.
- **Kacper Nizielski** (s4068858): NLP Engineer
  - Integrated the OpenAI API for chatbot responses.
  - Implemented fuzzy string matching using FuzzyWuzzy.
- **Melisa Uzun** (s3870618): Front-End Developer
  - Designed and implemented the responsive web interface.
  - Developed static files and templates for user interaction.
- **Duru Emekci** (s3844919): Data Analyst
  - Conducted data preprocessing and analysis.
  - Designed workflows for data extraction and transformation.

---

## How to Use the Project
### Prerequisites
Ensure you have the following installed on your system:
- Python 3.10+
- pip
- Redis (for Celery)

### Setup Instructions
1. **Install Dependencies**:
   Run the following command to install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the project root with the following keys:
   ```plaintext
    OPENAI_API_KEY_LEIDEN=<your_openai_api_key>
    DJANGO_SECRET_KEY=<your_django_secret_key>
    GOOGLE_API_KEY=<your_google_search_api_key>
    GOOGLE_CX=<your_google_cx>

   ```

3. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

---

## Key Features
- **Chatbot**: Answer questions about university schedules, staff, and facilities.
- **Event Management**: Upload and access academic schedules via MyTimeTable.
- **Dynamic Updates**: Automate database updates with Celery.
- **Responsive Design**: Access from desktop and mobile devices.

---

## Testing
### Unit Tests
Run unit tests for individual components:
```bash
python Profile_Scraper/unittest_scraper.py
```

### Django Tests
Perform end-to-end testing:
```bash
python manage.py test chatbot
python manage.py test landing
```

---

## Project Workflow
### Development Methodology
The project followed an Incremental Process Model:
1. **Core Features**: Initial chatbot integration and basic interface design.
2. **Enhanced Functionality**: Added NLP capabilities, web scraping, and dynamic updates.
3. **Testing and Refinement**: Conducted unit, integration, and system tests.
4. **Deployment**: Finalized a globally accessible platform.

### Tools Used
- **Django**: Backend framework for web application development.
- **SQLite3**: Lightweight database management.
- **Celery**: Task queue for periodic updates.
- **OpenAI API**: NLP-powered chatbot.
- **BeautifulSoup**: Web scraping.

---

## Accessing the Platform
The platform can be accessed locally or globally at:
- [Local Access](http://127.0.0.1:8000/)
- [Global Access](http://softdev.kooroshkz.com)