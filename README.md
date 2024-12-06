# UniVerse AI
## Leiden University Students AI-Powered Virtual Assistant
### SoftDev Project Group 11

---

UniVerse AI is a virtual assistant designed to enhance the academic experience for students at Leiden University. It leverages artificial intelligence to provide an intuitive chatbot, calendar integration, and other helpful features to streamline university-related tasks.

---

## Installation and Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd UniVerse-AI
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Collect static files:
    ```bash
    python manage.py collectstatic
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

6. Access the application at `http://127.0.0.1:8000/`.

---

## Features

- **Chatbot**: AI-powered assistant for students.
- **Calendar**: Integrated calendar for tracking exams, deadlines, and critical dates.
- **Text Completion**: Provides suggestions for predefined questions and completions.
- **Token Management**: Automatically handles message length and limits.
- **Responsive UI**: Ensures usability across devices.

---

## Improvements

- Automatically wrap long messages in the chatbot interface.
- Disable the 'Send' button and provide alerts when maximum tokens are reached.
- Add predefined questions for quick user assistance.
- Provide text completion suggestions.
- Introduce a calendar with critical information like exam dates.

---

## Team Members and Roles

### Koorosh
**Role**: DevOps Engineer  
Responsibilities: Infrastructure management, deployment, CI/CD pipelines.

### Diego
**Role**: Database Manager  
Responsibilities: Designing and managing the database schema, ensuring data integrity.

### Kacper
**Role**: API Data Extractor  
Responsibilities: Integration with external APIs and handling data pipelines.

### Emmanouil
**Role**: Backend Developer  
Responsibilities: Developing core application logic, API endpoints, and business logic.

### Duru
**Role**: Web Scraping Developer  
Responsibilities: Extracting and processing web data for use in the application.

### Melisa
**Role**: Front-End Developer  
Responsibilities: Designing and developing user interfaces for the application.
