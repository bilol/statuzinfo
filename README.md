
# Flask Company Info Application

## Overview

This Flask application displays information about companies and team members. It includes various pages such as an about page, team page, pricing page, partnerships page, and a company details page. The application uses Tailwind CSS for styling and Pandas for data handling.

## Features

- **Home Page**: Welcome page with navigation to other sections.
- **About Page**: Information about the company.
- **Team Page**: Displays team members with their details.
- **Pricing Page**: Shows different pricing plans.
- **Partnerships Page**: Showcases company partnerships.
- **Companies Page**: Lists all companies with an option to view details.
- **Company Details Page**: Detailed information about a specific company.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```bash
    flask run
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/` to view the application.

## File Structure

- `app.py`: The main Flask application file with route definitions.
- `templates/`: Directory containing HTML templates.
- `static/`: Directory containing static files (CSS, JS, images).
- `requirements.txt`: List of required Python packages.
- `README.md`: This file.

## Adding New Team Members

1. Add the team member's image to the `static/images/` directory.
2. Update the `team.html` file in the `templates/` directory with the new team member's information.

## License

This project is licensed under the MIT License.
