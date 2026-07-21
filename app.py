from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# The name of our "database" file
DATA_FILE = "courses.json"
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]

# ==========================================
# HELPER FUNCTIONS
# ==========================================


def read_courses():
    """Reads course data from the JSON file. Creates the file if it doesn't exist."""
    # Auto-create the file with an empty list if it doesn't exist yet
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w") as file:
                json.dump([], file)
        except IOError:
            raise Exception("Server Error: Could not create the courses.json file.")

    # Try to read and parse the JSON data
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError):
        raise Exception("Server Error: Could not read from the courses.json file.")


def write_courses(data):
    """Writes course data back to the JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except IOError:
        raise Exception("Server Error: Could not write to the courses.json file.")


def get_next_id(courses):
    """Finds the highest existing ID and adds 1. Starts at 1 if list is empty."""
    if not courses:
        return 1
    # Extract all the 'id' values and find the maximum, then add 1
    return max(course["id"] for course in courses) + 1


def validate_course_data(data):
    """Validates the incoming JSON data against our requirements."""
    if not data:
        return "No data provided"

    # 1. Check for missing required fields
    required_fields = ["name", "description", "target_date", "status"]
    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return f"Missing required field: {field}"

    # 2. Validate the status value
    if data["status"] not in VALID_STATUSES:
        return f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"

    # 3. Validate the date format (YYYY-MM-DD)
    try:
        datetime.strptime(data["target_date"], "%Y-%m-%d")
    except ValueError:
        return "Invalid target_date format. Must be YYYY-MM-DD"

    # Return None if there are no errors
    return None


# ==========================================
# API ENDPOINTS
# ==========================================


# GET / - Serve the frontend (index.html)
@app.route("/")
def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {"Content-Type": "text/html; charset=utf-8"}
    except FileNotFoundError:
        return "Frontend not found", 404
    except Exception as e:
        return f"Error loading frontend: {str(e)}", 500


# GET /api/courses - Retrieve all courses
@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    try:
        courses = read_courses()
        return jsonify(courses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /api/courses/<id> - Retrieve a specific course
@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_single_course(course_id):
    try:
        courses = read_courses()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Search for the course by ID
    for course in courses:
        if course["id"] == course_id:
            return jsonify(course), 200

    # If the loop finishes and we didn't return, the course doesn't exist
    return jsonify({"error": f"Course with ID {course_id} not found"}), 404


# POST /api/courses - Create a new course
@app.route("/api/courses", methods=["POST"])
def create_course():
    try:
        courses = read_courses()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    new_data = request.get_json()

    # Validate the incoming data using our helper function
    error_message = validate_course_data(new_data)
    if error_message:
        return jsonify({"error": error_message}), 400

    # Build the new course dictionary
    new_course = {
        "id": get_next_id(courses),
        "name": new_data["name"],
        "description": new_data["description"],
        "target_date": new_data["target_date"],
        "status": new_data["status"],
        # Generate the current UTC timestamp automatically
        "created_at": datetime.utcnow().isoformat() + "Z",
    }

    # Add the new course and save the file
    courses.append(new_course)
    try:
        write_courses(courses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(new_course), 201


# PUT /api/courses/<id> - Update an existing course
@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    try:
        courses = read_courses()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    update_data = request.get_json()

    # Validate the incoming data using our helper function
    error_message = validate_course_data(update_data)
    if error_message:
        return jsonify({"error": error_message}), 400

    # Search for the course to update
    for course in courses:
        if course["id"] == course_id:
            # Update the fields
            course["name"] = update_data["name"]
            course["description"] = update_data["description"]
            course["target_date"] = update_data["target_date"]
            course["status"] = update_data["status"]
            # Note: We purposely do not update 'id' or 'created_at'

            try:
                write_courses(courses)
                return jsonify(course), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return jsonify({"error": f"Course with ID {course_id} not found"}), 404


# DELETE /api/courses/<id> - Delete a course
@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        courses = read_courses()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Look for the index of the course we want to delete
    course_index = None
    for index, course in enumerate(courses):
        if course["id"] == course_id:
            course_index = index
            break

    if course_index is None:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404

    # Remove the course from the list
    deleted_course = courses.pop(course_index)

    try:
        write_courses(courses)
        # Return a success message and the data that was deleted
        return (
            jsonify(
                {"message": "Course successfully deleted", "course": deleted_course}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
