# Car Part Search Application

## Overview
This Flask application allows users to search for car parts across various platforms, including eBay, Amazon, Google, and RockAuto. Users can input their car details and receive relevant search results.

## Features
- Search for car parts by make, model, year, trim, and engine.
- Supports searching on multiple platforms.
- Scrapes data using Selenium for up-to-date results.

## Prerequisites
- Python 3.x
- Google Chrome browser
- ChromeDriver (compatible with your version of Chrome)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   Download and place chromedriver.exe in the same directory as Recon.py.

4. **Run the application**:
   ```bash
   python Recon.py

5. **Access the application**
   http://127.0.0.1:5000
