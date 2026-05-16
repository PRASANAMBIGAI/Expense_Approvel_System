# Expense Approval System - API Documentation

This document provides a comprehensive guide for frontend developers to integrate with the Expense Approval System backend.

## Base URL
`http://localhost:8000`

## Authentication & Authorization
The API uses **JWT (JSON Web Tokens)** for securing endpoints.
1. The frontend should call the `/auth/login` endpoint with the user's credentials to receive an `access_token`.
2. For all protected endpoints, the frontend must include this token in the HTTP Header:
   `Authorization: Bearer <your_access_token>`

*Note: Some endpoints require specific roles (`manager` or `admin`).*

---

## 1. Authentication Endpoints

### 1.1. Register a New User
* **Endpoint**: `POST /auth/register`
* **Auth Required**: No
* **Description**: Registers a new user (employee, manager, or admin) into the system.
* **Request Body (JSON)**:
  ```json
  {
    "employee_name": "John Doe",
    "employee_email": "john.doe@example.com",
    "password": "securepassword123",
    "role": "employee" // Options: "employee", "manager", "admin" (Defaults to "employee")
  }
  ```

### 1.2. Login
* **Endpoint**: `POST /auth/login`
* **Auth Required**: No
* **Description**: Authenticates a user and returns a JWT token.
* **Request Body (JSON)**:
  ```json
  {
    "employee_email": "john.doe@example.com",
    "password": "securepassword123"
  }
  ```
* **Response**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```

### 1.3. Get Current User Profile
* **Endpoint**: `GET /auth/me`
* **Auth Required**: Yes
* **Description**: Returns the profile details of the currently authenticated user.

---

## 2. Expenses Endpoints

### 2.1. Submit an Expense
* **Endpoint**: `POST /expenses/`
* **Auth Required**: Yes
* **Description**: Creates a new expense report. By default, its status will be `pending`.
* **Request Body (JSON)**:
  ```json
  {
    "title": "Flight to NY",
    "amount": 450.50,
    "description": "Business trip flight ticket",
    "category": "Travel"
  }
  ```

### 2.2. Get All Expenses
* **Endpoint**: `GET /expenses/`
* **Auth Required**: Yes
* **Description**: Returns a list of expenses. 
  - If the user is an `employee`, it should only return their own expenses.
  - If the user is a `manager` or `admin`, it will return expenses for their team.

### 2.3. Get a Single Expense
* **Endpoint**: `GET /expenses/{expense_id}`
* **Auth Required**: Yes
* **Description**: Retrieves the details of a specific expense by its ID.

### 2.4. Update an Expense
* **Endpoint**: `PUT /expenses/{expense_id}`
* **Auth Required**: Yes
* **Description**: Updates an existing expense. Usually, employees can only edit their expenses if the status is still `pending`.
* **Request Body (JSON)**:
  ```json
  {
    "title": "Flight to NY (Updated)",
    "amount": 470.00
  }
  ```

### 2.5. Delete an Expense
* **Endpoint**: `DELETE /expenses/{expense_id}`
* **Auth Required**: Yes
* **Description**: Deletes an expense. Only pending expenses can typically be deleted.

### 2.6. Approve an Expense
* **Endpoint**: `POST /expenses/{expense_id}/approve`
* **Auth Required**: Yes (Requires **`manager`** or **`admin`** role)
* **Description**: Approves a pending expense.
* **Request Body (JSON)**:
  ```json
  {
    "comment": "Approved as per policy."
  }
  ```

### 2.7. Reject an Expense
* **Endpoint**: `POST /expenses/{expense_id}/reject`
* **Auth Required**: Yes (Requires **`manager`** or **`admin`** role)
* **Description**: Rejects a pending expense. A comment is usually required.
* **Request Body (JSON)**:
  ```json
  {
    "comment": "Expense amount exceeds the standard limit."
  }
  ```

---

## 3. Categories Endpoints

### 3.1. Get All Categories
* **Endpoint**: `GET /categories/`
* **Auth Required**: Yes
* **Description**: Fetches the list of all available categories that employees can select when submitting an expense.
* **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Travel",
      "description": "Flight and taxi expenses"
    },
    {
      "id": 2,
      "name": "Meals",
      "description": "Business lunches"
    }
  ]
  ```

### 3.2. Add a New Category
* **Endpoint**: `POST /categories/`
* **Auth Required**: Yes (Requires **`admin`** role)
* **Description**: Adds a new category to the system.
* **Request Body (JSON)**:
  ```json
  {
    "name": "Software",
    "description": "Monthly software subscriptions"
  }
  ```

### 3.3. Update a Category
* **Endpoint**: `PUT /categories/{category_id}`
* **Auth Required**: Yes (Requires **`admin`** role)
* **Description**: Updates the name or description of an existing category.

### 3.4. Delete a Category
* **Endpoint**: `DELETE /categories/{category_id}`
* **Auth Required**: Yes (Requires **`admin`** role)
* **Description**: Deletes a category from the system.

---

## Important Types / Enums

The API uses standard strings for certain enum values.

**User Roles (`role`)**:
- `employee`
- `manager`
- `admin`

**Expense Status (`status`)**:
- `pending`
- `approved`
- `rejected`
