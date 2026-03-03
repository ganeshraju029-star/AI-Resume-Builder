from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import requests
import json
import os
from validation import validate_resume_data, sanitize_input

app = Flask(__name__)
CORS(app)

# Firebase Realtime Database Configuration
FIREBASE_DATABASE_URL = "https://ai-resume-builder-e120d-default-rtdb.firebaseio.com/"
FIREBASE_API_KEY = "your-api-key-here"  # You'll need to get this from Firebase Console

def firebase_request(path, method='GET', data=None):
    """Make requests to Firebase Realtime Database"""
    url = f"{FIREBASE_DATABASE_URL}{path}.json"
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        return response.json(), response.status_code
    except Exception as e:
        print(f"Firebase request error: {e}")
        return None, 500

@app.route("/")
def home():
    return "AI Resume Backend is running (Firebase Realtime Database)"

@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.json
    
    # Validate input
    errors = validate_resume_data(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    # Sanitize input
    name = sanitize_input(data.get("name", ""))
    education = sanitize_input(data.get("education", ""))
    skills = sanitize_input(data.get("skills", ""))
    projects = sanitize_input(data.get("projects", ""))
    goal = sanitize_input(data.get("goal", ""))

    resume_text = f"""
    {name}
    -------------------------
    Education:
    {education}

    Skills:
    {skills}

    Projects:
    {projects}

    Career Goal:
    {goal}
    """

    # Save to Firebase Realtime Database
    try:
        resume_id = str(uuid.uuid4())
        resume_data = {
            "id": resume_id,
            "name": name,
            "education": education,
            "skills": skills,
            "projects": projects,
            "goal": goal,
            "resume_text": resume_text.strip(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save to Firebase
        result, status = firebase_request(f"resumes/{resume_id}", 'PUT', resume_data)
        
        if status == 200:
            return jsonify({
                "resume": resume_text.strip(),
                "id": resume_id,
                "message": "Resume saved successfully!"
            })
        else:
            print(f"Firebase error: {result}")
            return jsonify({
                "resume": resume_text.strip(),
                "error": "Resume generated but not saved to Firebase"
            })
    except Exception as e:
        print(f"Error saving to Firebase: {e}")
        return jsonify({
            "resume": resume_text.strip(),
            "error": "Resume generated but not saved to database"
        })

# Get all resumes
@app.route("/resumes", methods=["GET"])
def get_all_resumes():
    try:
        result, status = firebase_request("resumes")
        
        if status == 200 and result:
            resumes = list(result.values()) if isinstance(result, dict) else []
            return jsonify({"resumes": resumes})
        else:
            return jsonify({"resumes": []})
    except Exception as e:
        print(f"Error fetching resumes: {e}")
        return jsonify({"error": "Failed to fetch resumes"}), 500

# Get a specific resume by ID
@app.route("/resumes/<resume_id>", methods=["GET"])
def get_resume(resume_id):
    try:
        result, status = firebase_request(f"resumes/{resume_id}")
        
        if status == 200 and result:
            return jsonify(result)
        else:
            return jsonify({"error": "Resume not found"}), 404
    except Exception as e:
        print(f"Error fetching resume: {e}")
        return jsonify({"error": "Failed to fetch resume"}), 500

# Update a resume
@app.route("/resumes/<resume_id>", methods=["PUT"])
def update_resume(resume_id):
    try:
        data = request.json
        
        # Validate input
        errors = validate_resume_data(data)
        if errors:
            return jsonify({"error": "Validation failed", "details": errors}), 400
        
        # Check if resume exists
        existing_result, existing_status = firebase_request(f"resumes/{resume_id}")
        if existing_status != 200 or not existing_result:
            return jsonify({"error": "Resume not found"}), 404
        
        # Sanitize input and update resume data
        update_data = {
            "id": resume_id,
            "name": sanitize_input(data.get("name", "")),
            "education": sanitize_input(data.get("education", "")),
            "skills": sanitize_input(data.get("skills", "")),
            "projects": sanitize_input(data.get("projects", "")),
            "goal": sanitize_input(data.get("goal", "")),
            "updated_at": datetime.now().isoformat()
        }
        
        # Regenerate resume text
        resume_text = f"""
        {update_data['name']}
        -------------------------
        Education:
        {update_data['education']}

        Skills:
        {update_data['skills']}

        Projects:
        {update_data['projects']}

        Career Goal:
        {update_data['goal']}
        """
        
        update_data["resume_text"] = resume_text.strip()
        
        # Update in Firebase
        result, status = firebase_request(f"resumes/{resume_id}", 'PUT', update_data)
        
        if status == 200:
            return jsonify({
                "message": "Resume updated successfully!",
                "resume": resume_text.strip()
            })
        else:
            return jsonify({"error": "Failed to update resume"}), 500
    except Exception as e:
        print(f"Error updating resume: {e}")
        return jsonify({"error": "Failed to update resume"}), 500

# Delete a resume
@app.route("/resumes/<resume_id>", methods=["DELETE"])
def delete_resume(resume_id):
    try:
        # Check if resume exists
        existing_result, existing_status = firebase_request(f"resumes/{resume_id}")
        if existing_status != 200 or not existing_result:
            return jsonify({"error": "Resume not found"}), 404
        
        # Delete from Firebase
        result, status = firebase_request(f"resumes/{resume_id}", 'DELETE')
        
        if status == 200:
            return jsonify({"message": "Resume deleted successfully!"})
        else:
            return jsonify({"error": "Failed to delete resume"}), 500
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return jsonify({"error": "Failed to delete resume"}), 500

if __name__ == "__main__":
    print("Starting AI Resume Backend (Firebase Realtime Database)")
    print(f"Connected to: {FIREBASE_DATABASE_URL}")
    print("Note: Make sure your Firebase Realtime Database rules allow read/write access")
    app.run(debug=True, host="0.0.0.0", port=5000)
