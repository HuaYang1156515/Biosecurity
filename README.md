# Ocean Pest and Disease Biosecurity Guide

This Flask web application functions as a biosecurity guide, providing information on ocean pests and diseases present in New Zealand, as well as those that are not found in the country.

## Project Structure

The project is structured as follows:
- `app.py`: The main Flask application file.
- `templates/`: Folder containing the HTML templates for rendering views.
- `static/`: Folder containing static files like CSS, JavaScript, and images.
- `connect.py`: Module that stores database connection parameters.
- `biosecurity.sql`: MySQL script for creating and populating the database.

## Setup and Installation

To run this application, you need Python installed on your system. The dependencies are listed in the `requirements.txt` file.

1. Clone the repository to your local machine.
2. Create a virtual environment:
3. Activate the virtual environment:
- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On Unix or MacOS:
  ```
  source venv/bin/activate
  ```
4. Install the required packages:
5. Set up your MySQL database using the `biosecurity.sql` script.

## Running the Application

To run the application:
Or directly with python:

The application will be accessible at `localhost:5000` by default.

## Features

- User authentication system with login and registration functionalities.
- Role-based access control for different user roles: Mariners, Staff, and Administrators.
- Responsive design with a marine theme.
- CRUD operations on ocean pests and diseases.

## Database Connection

The `get_db_connection` function in `app.py` sets up the database connection using credentials from `connect.py`. Make sure to update `connect.py` with your database credentials.


