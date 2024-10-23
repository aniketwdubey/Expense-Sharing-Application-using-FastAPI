
# Daily Expenses Sharing Application

## Overview
This is a backend service for managing and sharing daily expenses between users. The application allows users to add expenses and split them in three different ways: equally, by exact amounts, or by percentage. It also manages user details, validates input, and generates a downloadable balance sheet.

### Key Features:
- **User Management:** Create, retrieve, and manage users.
- **Expense Management:** Add expenses with various split methods.
- **Balance Sheet:** Track individual expenses, total expenses, and download balance sheets.

## Project Structure
```
├── README.md
├── app
│   ├── api
│   │   ├── users.py            # API logic for user management
│   │   ├── expenses.py         # API logic for expenses
│   │   └── users.py            # API logic for balance management
│   ├── core
│   │   └── database.py         # Database connection setup
│   ├── main.py                 # Application entry point
│   ├── models
│   │   └── models.py           # Database models for users, expenses, and balances
│   └── schemas
│       ├── users.py            # Pydantic models for user creation
│       ├── expenses.py         # Pydantic models for expense creation
│       └── balance.py          # Pydantic models for balance creation
└── requirements.txt            # Required Python packages
```

## Setup and Installation

### 1. Clone the repository
```
git clone <repository-url>
cd <repository-directory>
```

### 2. Install dependencies
Ensure you have Python 3.9+ installed. Install the required packages:
```
pip install -r requirements.txt
```

### 3. Database Setup
This application uses PostgreSQL as the database. Make sure PostgreSQL is installed and running on your machine.

Create a new PostgreSQL database and update the `SQLALCHEMY_DATABASE_URL` in `app/core/database.py` to match your PostgreSQL credentials:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@localhost:5432/<database>"
```

### 4. Run the Application
Start the FastAPI server:
```
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### 6. Data Models
#### Users
- **User**: Contains `id`, `name`, `email`, and `mobile`.

#### Expenses
- **Expense**: Contains `id`, `amount`, `description`, `paid_by`, `split_method`, and `user_ids`.

#### Balance
- **Balance**: Tracks the balance for each user, including the `user_id`, `user_name`, and `amount_owed`.

### 5. API Endpoints
The API endpoints are organized as follows:

#### User Endpoints:
- `POST /users/`: Create a new user.
- `GET /users/{user_id}`: Retrieve details of a specific user.
- `GET /users/`: Retrieve all users.

#### Expense Endpoints:
- `POST /expenses/`: Add a new expense.
- `GET /expenses/{user_id}`: Retrieve individual expenses for a user.
- `GET /expenses/`: Retrieve overall expenses.

#### Balance Sheet Endpoints:
- `GET /balance/{user_id}`: Retrieve the balance sheet for a specific user.
- `GET /balance/`: Retrieve overall balances for all users.
- `GET /download`: Download the balance sheet as a file.


### 6. Example Usage

#### Add a User
![alt text](<screenshots/Screenshot 2024-10-23 at 5.46.01 PM.png>)

#### Users Table
![alt text](<screenshots/Screenshot 2024-10-23 at 5.49.17 PM.png>)

#### Add Expenses
![alt text](<screenshots/Screenshot 2024-10-23 at 7.14.39 PM.png>)
![alt text](<screenshots/Screenshot 2024-10-23 at 6.39.26 PM.png>)
![alt text](<screenshots/Screenshot 2024-10-23 at 6.47.22 PM.png>)

#### Expenses Table
![alt text](<Screenshot 2024-10-23 at 6.47.43 PM.png>)

#### Retrieve overall expenses.
![alt text](<screenshots/Screenshot 2024-10-23 at 7.24.43 PM.png>)

#### Retrieve individual user expenses.
![alt text](<screenshots/Screenshot 2024-10-23 at 7.23.06 PM.png>)

#### Balance Sheet - Show overall expenses for all users.
![alt text](<screenshots/Screenshot 2024-10-23 at 7.28.37 PM.png>)

#### Balance Table
![alt text](<screenshots/Screenshot 2024-10-23 at 6.47.48 PM.png>)

<!-- ### 7. Data Validation
The application ensures the following:
- **User input validation**: Email and mobile numbers must be unique.
- **Split validation**: For percentage splits, the total must add up to 100%.

## Bonus Features
- **Error handling**: The application includes basic error handling.
- **Input validation**: Data is validated before being processed.
- **Downloadable balance sheets**: Users can download a detailed balance sheet.
  
### Potential Improvements:
- **Authentication and Authorization**: Secure the API with user authentication.
- **Performance Optimization**: Add caching for large datasets.
- **Testing**: Unit and integration tests can be added for better reliability. -->

## License
This project is licensed under the MIT License.
