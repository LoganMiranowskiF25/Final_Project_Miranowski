### INF601 - Advanced Programming with Python
### Logan Miranowski
### Final Project - Aviation Inventory Management Project (AIM)

# Aviation Inventory Management System

A Streamlit web app for managing aviation parts inventory with expiration tracking, low stock alerts, and FAA aircraft registry lookup.

### Description


This project is a Python-based inventory management system designed to:
- Add, view, update, and delete aviation inventory items
- Track expiration dates on time-sensitive components
- Alert users when stock falls below reorder thresholds
- Look up aircraft registrations through FAA Aircraft Registry API
- Store all inventory data persistently using SQLite

The goal was to demonstrate Python knowledge, modular application design, database and API integration

### Getting Started

### Dependencies
* Python 3.12+
* Streamlit
* Requests
* SQLite3 (built into Python)

> ALL dependencies listed in 'requirements.txt'

### Installation
* Clone this repository:
'''bash
git clone
cd Final_Project_Miranowski

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1 # Windows PS
# OR
source venv/bin/activate # macOS/Linux

# Install required packages
pip install -r requirements.txt

# Run app
streamlit run app.py

### Usage
* Open browser and navigate to 'http://localhost:8501'
* Use sidebar to navigate between features

### Author

### Version History
* 1.0
    * Final version will fully functional inventory management system
* 0.9
    * Added FAA registry API lookup
* 0.8
    * Fixed nested button issue in API section using session state
* 0.7
    * Added low stock expiration and alert features
* 0.6
    * Implemented search, delete, and update functions
* 0.5
    * Initial commit with database setup and add/view features

### License
* N/A

### Acknowledgements
* Streamlit doc: https://docs.streamlit.io/
* FAA Aircraft Registry: https://registry.faa.gov/
* SQLite3 doc: https://docs.python.org/3/library/sqlite3.html