# File Sharing Tool

The Web-Based File-Sharing Tool is a web application that allows users to upload files and share them with multiple recipients via email. Users can log in to the website, choose a file from their local storage, enter up to 5 email addresses, and upload the file to Amazon S3. The application then sends an email to each provided email address containing a link to the uploaded file.

## Features

- User registration: Users can sign up for an account by providing their full name, email, and password.
- User authentication: Users can sign up and log in to the application using their email and password.
- File upload: Users can select a file from their local storage and upload it to Amazon S3.
- Email sharing: Users can enter up to 5 email addresses, and the application will send an email to each recipient with a link to the uploaded file.
- Secure file storage: Uploaded files are stored securely in Amazon S3.

## Technologies used

- Python
- Flask (Backend)
- Flask-Login
- Flask-Bcrypt
- Flask-SQLAlchemy
- Flask-WTF
- AWS S3
- HTML, CSS, JavaScript (Frontend)
- AWS SES
- Dynamo DB

## Installation

1. Navigate to the project directory: `cd file-sharing-tool`
2. Install the required packages: `pip install -r requirements.txt`
3. Create a `.env` file with the following variables:

   ```bash
   SECRET_KEY=your-secret-key
   SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
   AWS_ACCESS_KEY_ID = access_key
   AWS_SECRET_ACCESS_KEY = secret_key
   AWS_DEFAULT_REGION = "us-east-1"
   AWS_BUCKET_NAME = "cloud-sharing-tool"
   ```

## Usage

To run the app, use the following command: `flask run`

The app will be available at `http://localhost:5000/`

1. Register a new account.
2. Log in to the application.
3. Upload a file.
4. Enter up to 5 email addresses separated by commas.
5. Click on the "Upload" button.
6. The application will send an email to each recipient with a link to the uploaded file.
7. Check your email inbox.

## Project Structure

```bash
.
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── app
│   ├── auth.py
│   ├── cloud_utils.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
│
├── static
│   ├── main.css
│   └── main.js
│
├── templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── shared_files.html
│   └── upload.html
│
└── instance
    └── site.db
```

## Project Components

1. .env: This file stores environment variables, such as AWS credentials or database configurations. Make sure to keep this file secure and never commit it to version control.

2. .gitignore: This file specifies files and directories that should be ignored by Git version control. Commonly ignored files include virtual environments, database files, and sensitive credentials.

3. README.md: This file contains project documentation, including the project description, installation instructions, usage guide, and any other relevant information.

4. requirements.txt: This file lists all the Python dependencies required to run the project. Use pip to install these dependencies.

5. run.py: This script is the entry point to the application. It contains the code to run the Flask app.

6. app: This directory contains the application's main logic and components.

   - auth.py: This module handles user authentication and user-related functionalities.
   - cloud_utils.py: This module provides utility functions for interacting with cloud services like AWS S3 and SES.
   - forms.py: This module defines the Flask-WTF forms used in the application.
   - models.py: This module defines the data models or database tables used in the application (if applicable).
     routes.py: This module defines the Flask routes and views for the application.
   - **init**.py: This script initializes the Flask application and configures it.
   - static: This directory contains static files like CSS and JavaScript used in the frontend.

   - templates: This directory contains the HTML templates for rendering the views of the application.

7. instance: This directory contains the application instance folder, which can store the SQLite database (e.g., site.db).
