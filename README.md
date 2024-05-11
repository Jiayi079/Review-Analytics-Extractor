# Project Presentation Link
[OneDrive Link](https://uillinoisedu-my.sharepoint.com/:v:/g/personal/jiayigu4_illinois_edu/Ea_tXnUMB1FKrO0pBf4Vug4BnQwv5lcWpQbiDn6f8b8hcQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=XlCgAr).


# Project Setup Guide

This README.md file includes all necessary steps to set up and run your project, along with troubleshooting tips to handle common issues.


## Setting Up the Project Environment

### Prerequisites
- **Python**: Ensure Python is installed on your machine. Download from [python.org](https://www.python.org/downloads/).
- **MongoDB**: Install MongoDB locally or have access to a MongoDB server. Installation instructions are available on the [MongoDB website](https://docs.mongodb.com/manual/installation/).
- **Git**: Install Git to clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).

### Clone the Repository
Clone the project repository by running:
```bash
git clone [URL-to-your-GitHub-repository]
```

### Install Dependencies
Navigate to the project directory and set up a virtual environment:
```bash
cd ./project-root
python -m venv venv     # Activate the virtual environment

# On Windows:
.\venv\Scripts\Activate.ps1
# On MacOS/Linux:
source venv/bin/Activate.ps1
```


Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Configuring the Project


### Environment Variables
Ensure the '.env' file is properly set up in the project directory:
```bash
MONGO_URI=mongodb://localhost:27017/reviewDatabase
```


### MongoDB Setup
Ensure MongoDB is running and the required databases and collections are created.

## Running the Flask Application

### Start the Flask App
From the project directory, where 'app.py' is located, run:
```bash
python .\backend\app.py
```
This starts the Flask server, accessible from http://127.0.0.1:5000/ on your web browser.

### Accessing the Application
Open a web browser and navigate to http://127.0.0.1:5000/ to interact with the application.

## Common Troubleshooting
- **Python or Pip Not Found**: Make sure Python and pip are installed correctly and added to your system’s PATH.Download from [python.org](https://www.python.org/downloads/).
- **MongoDB Connection Issues**: Check that MongoDB is running and the URI in the .env file matches your MongoDB configuration.
- **Dependencies Not Installed**: Ensure all required Python libraries are installed by re-running pip install -r requirements.txt in your virtual environment.
