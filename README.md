# Ocean Pest and Disease Biosecurity Guide

This Flask web application functions as a biosecurity guide, providing information on ocean pests and diseases present in New Zealand, as well as those that are not found in the country.


## Comments

## Application Functionality

### Database Connection
- `get_db_connection()`: Connects to the MySQL database using configuration from `connect.py`.

### Authentication
- `hash_password(password)`: Creates a hash of the provided password with a salt.
- `check_password(input_password, stored_hash)`: Compares the provided password against the stored hash for authentication.

### Routes
- `home()`: Serves the home page with a marine-themed design.
- `login()`: Manages the login process, authenticating users and redirecting to their dashboard.
- `logout()`: Ends the user's session and redirects to the home page.
- `register()`: Handles new user registration with password hashing and profile creation.

### User Role Management
- `role_required(role)`: Decorator to enforce role-based access control on routes.
- `get_user_role(user_id)`: Retrieves the role associated with a user ID from the database.

### Dashboards
- `dashboard()`: Displays the general dashboard after user login.
- `mariner_dashboard()`: Shows the dashboard for users with the Mariner role.
- `staff_dashboard()`: Renders the Staff-specific dashboard.
- `admin_dashboard()`: Presents the dashboard for users with the Administrator role.

### User Profile
- `profile()`: Enables users to view and update their profile information.
- `change_password()`: Allows users to change their account password.

### Ocean Guide
- `guide()`: Lists ocean pests and diseases from the biosecurity guide.
- `guide_detail(pest_id)`: Provides detailed information about a specific ocean pest or disease.
- `get_all_pests_from_db()`: Fetches all pest and disease records from the database.
- `get_pest_detail_from_db(pest_id)`: Retrieves detailed data for an individual pest or disease entry.


## Project Structure

The project is structured as follows:
- `app.py`: The main Flask application file.
- `templates/`: Folder containing the HTML templates for rendering views.
- `static/`: Folder containing static files like CSS, JavaScript, and images.
- `connect.py`: Module that stores database connection parameters.
- `biosecurity.sql`: MySQL script for creating and populating the database.

## Setup  Installation and Run

1. Clone the repository
2. Create a virtual environment
3. Activate the virtual environment
4. Install the required packages, pip are listed in the `requirements.txt` file
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
