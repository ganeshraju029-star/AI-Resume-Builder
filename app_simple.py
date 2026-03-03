from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import json
import os
from validation import validate_resume_data, sanitize_input

app = Flask(__name__)
CORS(app)

# Simple file-based storage for testing (without Firebase)
DATA_FILE = "resumes_data.json"

def load_resumes():
    """Load resumes from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_resumes(resumes):
    """Save resumes to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(resumes, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving resumes: {e}")
        return False

@app.route("/")
def home():
    return "AI Resume Backend is running (Simple Mode - File Storage)"

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

    # Save to file (simulating Firebase)
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
        
        resumes = load_resumes()
        resumes.append(resume_data)
        save_resumes(resumes)
        
        return jsonify({
            "resume": resume_text.strip(),
            "id": resume_id,
            "message": "Resume saved successfully!"
        })
    except Exception as e:
        print(f"Error saving resume: {e}")
        return jsonify({
            "resume": resume_text.strip(),
            "error": "Resume generated but not saved to database"
        })

# Get all resumes
@app.route("/resumes", methods=["GET"])
def get_all_resumes():
    try:
        resumes = load_resumes()
        return jsonify({"resumes": resumes})
    except Exception as e:
        print(f"Error fetching resumes: {e}")
        return jsonify({"error": "Failed to fetch resumes"}), 500

# Get a specific resume by ID
@app.route("/resumes/<resume_id>", methods=["GET"])
def get_resume(resume_id):
    try:
        resumes = load_resumes()
        resume = next((r for r in resumes if r["id"] == resume_id), None)
        
        if resume:
            return jsonify(resume)
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
        
        resumes = load_resumes()
        resume_index = next((i for i, r in enumerate(resumes) if r["id"] == resume_id), None)
        
        if resume_index is None:
            return jsonify({"error": "Resume not found"}), 404
        
        # Sanitize input and update resume data
        update_data = {
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
        
        # Update the resume
        resumes[resume_index].update(update_data)
        save_resumes(resumes)
        
        return jsonify({
            "message": "Resume updated successfully!",
            "resume": resume_text.strip()
        })
    except Exception as e:
        print(f"Error updating resume: {e}")
        return jsonify({"error": "Failed to update resume"}), 500

# Delete a resume
@app.route("/resumes/<resume_id>", methods=["DELETE"])
def delete_resume(resume_id):
    try:
        resumes = load_resumes()
        resume_index = next((i for i, r in enumerate(resumes) if r["id"] == resume_id), None)
        
        if resume_index is None:
            return jsonify({"error": "Resume not found"}), 404
        
        del resumes[resume_index]
        save_resumes(resumes)
        
        return jsonify({"message": "Resume deleted successfully!"})
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return jsonify({"error": "Failed to delete resume"}), 500

if __name__ == "__main__":
    print("Starting AI Resume Backend (Simple Mode - File Storage)")
    print("Note: This is running without Firebase. Install Microsoft Visual C++ Build Tools to use Firebase.")
    app.run(debug=True, host="0.0.0.0", port=5000)
