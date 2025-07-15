# Freelance Project Tracker

A full-stack application built using **Flask** and **MongoDB** for managing freelance projects. 
It helps freelancers keep track of their work, update project statuses, and view total earnings.
The frontend is created using **HTML**, **CSS**, and **JavaScript**, making it easy to interact with the backend APIs.

---

## Features

- Add or update freelance projects with client name, status, deadline, and amount.
- View a list of active (pending) projects.
- Mark projects as "Completed" with one click.
- Calculate and display total earnings from completed projects.
- Built-in form validation and date restriction.
- Backend APIs built with Flask and connected to MongoDB Atlas.
- Environment variables handled securely using `.env`.

---

## Tech Stack

| Layer         | Technology               |
|--------------|---------------------------|
| Backend       | Flask, Python             |
| Database      | MongoDB Atlas             |
| Frontend      | HTML, CSS, JavaScript     |
| Styling       | Custom CSS                |
| API Comm      | Fetch API (JSON)          |
| Secret Mgmt   | python-dotenv (.env)      |

---

---

Setup Instructions
1. Clone the Repository

bash
git clone https://github.com/gagandeep1763/Freelance-Project-Tracker.git
cd Freelance-Project-Tracker

2. Create & Activate Virtual Environment

python -m venv venv

source venv/bin/activate   

# On Windows: venv\Scripts\activate

3: Install Python Dependencies

From your project root folder:

pip install flask flask-cors pymongo python-dotenv

4: Create MongoDB Database on MongoDB Atlas

Go to: https://www.mongodb.com/cloud/atlas

Sign up / Log in

5. Create a Free Cluster:

Click "Build a Database"
Choose "Shared" (free tier)
Select cloud provider + region (choose nearest to you)
Name your cluster (e.g., Cluster0)
Click Create

Create a Database User:
Go to Database Access (left panel)

Click “+ ADD NEW DATABASE USER”
Set username and password 

Role: Read and Write to Any Database
Click Add User

Allow Your IP Address:
Go to Network Access
Click “ADD IP ADDRESS”
Click “ALLOW ACCESS FROM ANYWHERE” (0.0.0.0/0) (for development only)
Click Confirm
Get Your Connection String:
Go to Database > Connect > Drivers
Choose Python, version 3.6+

Copy the connection URI. It will look like this:

mongodb+srv://<username>:<password>@cluster0.ahac7me.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

6. : Secure Your MongoDB Credentials with .env
Create a file named .env in your project root.
Paste your MongoDB username and password:

MONGO_USER=
MONGO_PASS=

Important: Make sure your .gitignore file contains:

7: Test Everything
Run Flask:

python app.py
Open frontend.html in browser.

Use Developer Tools > Network Tab to verify API calls are reaching http://localhost:5000.



