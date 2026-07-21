# 🚀 CodeCraftHub

Welcome to **CodeCraftHub**! This is a simple, beginner-friendly REST API built with Python and Flask. It is designed to help developers track the programming courses they want to learn. 

Instead of dealing with complex databases or authentication, this project stores all data in a simple JSON text file (`courses.json`), making it the perfect starting point for learning how REST APIs work!

---

## ✨ Features
*   **Full CRUD Operations:** Create, Read, Update, and Delete courses.
*   **Simple Storage:** Uses a flat JSON file (`courses.json`) as a database. (Auto-generates if it doesn't exist).
*   **Auto-Generated IDs & Timestamps:** Automatically assigns sequential IDs and creation timestamps to new courses.
*   **Data Validation:** Prevents bad data by validating required fields, date formats (YYYY-MM-DD), and course statuses.
*   **Comprehensive Error Handling:** Returns clear, readable error messages and proper HTTP status codes.

---

## 🛠️ Project Structure

Here is how the project is organized:

```text
codecraft-hub/
├── app.py             # The main Flask application containing all API routes and logic
├── courses.json       # (Auto-generated) The text file where all course data is saved
└── requirements.txt   # A list of Python dependencies required to run the project
```

---

## 💻 Installation Instructions

Follow these step-by-step instructions to get the project running on your local machine.

**Prerequisites:** You must have Python installed on your computer. You can download it from [python.org](https://www.python.org/).

1. **Create a project folder:**
   ```bash
   mkdir codecraft-hub
   cd codecraft-hub
   ```

2. **Create a virtual environment (Recommended):**
   A virtual environment keeps your project dependencies separate from other Python projects.
   *   **Windows:** `python -m venv venv`
   *   **Mac/Linux:** `python3 -m venv venv`

3. **Activate the virtual environment:**
   *   **Windows:** `venv\Scripts\activate`
   *   **Mac/Linux:** `source venv/bin/activate`

4. **Install Flask:**
   ```bash
   pip install Flask
   ```

5. **Create the application file:**
   Create a file named `app.py` in your folder and paste the complete Python Flask code into it.

---

## ▶️ How to Run the Application

1. Open your terminal or command prompt.
2. Ensure you are in the `codecraft-hub` folder and your virtual environment is activated.
3. Run the following command:
   ```bash
   python app.py
   ```
4. You should see output indicating that the Flask server is running, usually at: 
   `* Running on http://127.0.0.1:5000`

> **Note:** The server will keep running in your terminal. To stop it, press `Ctrl + C`.

---

## 📖 API Endpoints Documentation

The base URL for all endpoints is `http://127.0.0.1:5000`

### 1. Get All Courses
*   **Endpoint:** `/api/courses`
*   **Method:** `GET`
*   **Description:** Returns a list of all saved courses.
*   **Success Response:** `200 OK` (Returns an array of course objects)

### 2. Get a Specific Course
*   **Endpoint:** `/api/courses/<id>`
*   **Method:** `GET`
*   **Description:** Returns the details of a single course by its ID.
*   **Success Response:** `200 OK`
*   **Error Response:** `404 Not Found` (If the ID does not exist)

### 3. Create a New Course
*   **Endpoint:** `/api/courses`
*   **Method:** `POST`
*   **Description:** Adds a new course to your list.
*   **Required JSON Payload:**
    ```json
    {
        "name": "Course Name",
        "description": "What you will learn",
        "target_date": "YYYY-MM-DD",
        "status": "Not Started" 
    }
    ```
    *(Note: Status must be "Not Started", "In Progress", or "Completed")*
*   **Success Response:** `201 Created`

### 4. Update a Course
*   **Endpoint:** `/api/courses/<id>`
*   **Method:** `PUT`
*   **Description:** Updates an existing course. You must provide all required fields in the payload.
*   **Required JSON Payload:** Same as POST request.
*   **Success Response:** `200 OK`

### 5. Delete a Course
*   **Endpoint:** `/api/courses/<id>`
*   **Method:** `DELETE`
*   **Description:** Permanently removes a course.
*   **Success Response:** `200 OK`

---

## 🧪 Testing Instructions

Because web browsers only send `GET` requests by default, you cannot test `POST`, `PUT`, or `DELETE` by typing the URL into your browser address bar. 

### Option 1: Using Command Line (`curl`)
You can use the built-in terminal tool called `curl`. Open a *new* terminal window (leave the one running your Flask server open) and try adding a course:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
-H "Content-Type: application/json" \
-d '{
    "name": "Mastering REST APIs",
    "description": "Learn to build and test APIs using Flask and Python.",
    "target_date": "2026-12-31",
    "status": "Not Started"
}'
```

### Option 2: Using an API Client (Recommended for Beginners)
Visual tools make it much easier to interact with APIs. We highly recommend downloading **[Postman](https://www.postman.com/)** or **[Insomnia](https://insomnia.rest/)**. 
1. Open the tool.
2. Select your HTTP Method (e.g., POST).
3. Enter the URL (`http://127.0.0.1:5000/api/courses`).
4. Go to the "Body" tab, select "raw" and "JSON".
5. Paste your JSON data and click "Send"!

---

## ⚠️ Troubleshooting Common Issues

**1. `Address already in use` error when starting the server**
*   **Cause:** Another program is already using port 5000.
*   **Fix:** Stop the other program, or change the port Flask runs on by modifying the last line of `app.py` to: `app.run(debug=True, port=5001)`

**2. `ModuleNotFoundError: No module named 'flask'`**
*   **Cause:** Flask is not installed, or you forgot to activate your virtual environment.
*   **Fix:** Ensure your virtual environment is activated (step 3 of installation) and run `pip install Flask` again.

**3. `400 Bad Request` when sending a POST/PUT request**
*   **Cause:** The JSON data you sent is missing a required field, has a typo, or has an invalid date format/status.
*   **Fix:** Read the error message returned by the API—it will tell you exactly which field is missing or invalid! Ensure your headers are set to `Content-Type: application/json` if using curl or Postman.

**4. Data isn't saving!**
*   **Cause:** If the application crashes unexpectedly, file handles might not close. However, the app writes immediately on every POST/PUT/DELETE. 
*   **Fix:** Check if your folder requires administrator/root permissions to create files, though this is rare on standard user folders.
