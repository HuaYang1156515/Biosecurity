# Ocean Pest and Disease Biosecurity Guide

This Flask web application functions as a biosecurity guide, providing information on ocean pests and diseases present in New Zealand, as well as those that are not found in the country.

## Project Structure

The project is structured as follows:
- `app.py`: The main Flask application file.
- `templates/`: Folder containing the HTML templates for rendering views.
- `static/`: Folder containing static files like CSS, JavaScript, and images.
- `connect.py`: Module that stores database connection parameters.
- `biosecurity.sql`: MySQL script for creating and populating the database.

## Setup  Installation and Run

To run this application, Python need be installed. The pip are listed in the `requirements.txt` file.

1. Clone the repository
2. Create a virtual environment
3. Activate the virtual environment
4. Install the required packages
5. Set up MySQL database using the `biosecurity.sql` script
6. The application will be accessible at `localhost:5000` by default.

## Functions

- `get_db_connection()`: Establishes a connection to the MySQL database 
- `hash_password(password)`: Generates a hashed password, using salt
- `check_password(input_password, stored_hash)`: password 
- `home()`: homepage 
- `login()`: user login 
- `logout()`: user logs out 
- `register()`: user registration 
- `role_required(role)`: restricts access to certain views based on user role
- `dashboard()`:view after a user logs in
--- `mariner_dashboard()`
--- `staff_dashboard()`
--- `admin_dashboard()`
- `get_user_role(user_id)`: Retrieves the role from the database based on the user's ID.
- `profile()`:view and update profile information
- `change_password()`: password
- `guide()`: Displays ocean pests
- `guide_detail(pest_id)`: detailed information 
- `get_all_pests_from_db()`: Retrieves all pest entries from the database.
- `get_pest_detail_from_db(pest_id)`: Fetches data 
