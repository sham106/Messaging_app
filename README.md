# Messaging app

## Introduction
Thank you for exploring the CS Messaging Web App project! This web application is designed to handle a high volume of customer inquiries and streamline communication between customers and agents. The main features include responding to customer messages, flagging urgent issues, and providing a scalable solution for a growing customer base.

## Getting Started

Follow these instructions to set up and run the solution on your local machine.

### Prerequisites

Make sure you have the following installed:

- Python 
- Django 
- NLTK library (for natural language processing)
- Virtual Environment
- Mysql
- Django API Framework
- Panda (importing xlsx fie)

### Additional Features
- Ability to divide work among agents
- Can  surface messages that are more urgent and in need of immediate attention. 
- search functionality to allow agents to search over incoming messages and / or customers


### How to set up the application
 1. Clone the reposit 
 ```    git clone https://github.com/sham106/Messaging_app.git ```
2. Navigate to the project directory: ``` cd Messaging_app.git ```
3. Install dependencies: ```pip install -r requirements.txt```
4. Apply migrations:
    ```python manage.py migrate```
5. Load initial data (if any):
  ```python manage.py loaddata initial_data.json```
6. Running the Application
#### Start the development server
  ```python manage.py runserver```
  
  Access the application at ```http://localhost:8000.```


