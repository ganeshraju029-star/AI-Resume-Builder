from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
from validation import validate_resume_data, sanitize_input
import os

app = Flask(__name__)
CORS(app)  # allow frontend to talk to backend

# Mock database for demo (since Firebase has installation issues)
resumes_db = {}

@app.route("/")
def home():
    return "AI Resume Backend is running"

@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    if not resumes_db:
        return jsonify({"error": "Database not available"}), 500
    
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

    # Save to Firebase
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
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        db.collection("resumes").document(resume_id).set(resume_data)
        
        return jsonify({
            "resume": resume_text.strip(),
            "id": resume_id,
            "message": "Resume saved successfully!"
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
    if not db:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        resumes = []
        docs = db.collection("resumes").stream()
        
        for doc in docs:
            resume_data = doc.to_dict()
            # Convert datetime objects to strings for JSON serialization
            if 'created_at' in resume_data:
                resume_data['created_at'] = resume_data['created_at'].isoformat()
            if 'updated_at' in resume_data:
                resume_data['updated_at'] = resume_data['updated_at'].isoformat()
            resumes.append(resume_data)
        
        return jsonify({"resumes": resumes})
    except Exception as e:
        print(f"Error fetching resumes: {e}")
        return jsonify({"error": "Failed to fetch resumes"}), 500

# Get a specific resume by ID
@app.route("/resumes/<resume_id>", methods=["GET"])
def get_resume(resume_id):
    if not db:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        doc = db.collection("resumes").document(resume_id).get()
        
        if doc.exists:
            resume_data = doc.to_dict()
            # Convert datetime objects to strings
            if 'created_at' in resume_data:
                resume_data['created_at'] = resume_data['created_at'].isoformat()
            if 'updated_at' in resume_data:
                resume_data['updated_at'] = resume_data['updated_at'].isoformat()
            return jsonify(resume_data)
        else:
            return jsonify({"error": "Resume not found"}), 404
    except Exception as e:
        print(f"Error fetching resume: {e}")
        return jsonify({"error": "Failed to fetch resume"}), 500

# Update a resume
@app.route("/resumes/<resume_id>", methods=["PUT"])
def update_resume(resume_id):
    if not db:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        data = request.json
        
        # Validate input
        errors = validate_resume_data(data)
        if errors:
            return jsonify({"error": "Validation failed", "details": errors}), 400
        
        doc_ref = db.collection("resumes").document(resume_id)
        
        # Check if resume exists
        if not doc_ref.get().exists:
            return jsonify({"error": "Resume not found"}), 404
        
        # Sanitize input and update resume data
        update_data = {
            "name": sanitize_input(data.get("name", "")),
            "education": sanitize_input(data.get("education", "")),
            "skills": sanitize_input(data.get("skills", "")),
            "projects": sanitize_input(data.get("projects", "")),
            "goal": sanitize_input(data.get("goal", "")),
            "updated_at": datetime.now()
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
        
        doc_ref.update(update_data)
        
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
    if not db:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        doc_ref = db.collection("resumes").document(resume_id)
        
        # Check if resume exists
        if not doc_ref.get().exists:
            return jsonify({"error": "Resume not found"}), 404
        
        doc_ref.delete()
        
        return jsonify({"message": "Resume deleted successfully!"})
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return jsonify({"error": "Failed to delete resume"}), 500

# Chatbot endpoint
@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.json
        user_message = sanitize_input(data.get("message", ""))
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # System prompt for the chatbot
        system_prompt = """You are an AI assistant for the AI Resume & Portfolio Builder application. 
        You help users with:
        - Resume building tips and best practices
        - Career advice and guidance
        - Skill development suggestions
        - Project ideas and recommendations
        - Education and career path planning
        - Answering questions about the resume building process
        
        Be helpful, professional, and provide actionable advice. Keep responses concise but informative."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content.strip()
        
        return jsonify({
            "response": bot_response,
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error in chatbot: {e}")
        # Fallback response if OpenAI fails
        fallback_responses = [
            "I'm here to help with your resume building! Feel free to ask me about career advice, skill recommendations, or resume tips.",
            "As your AI resume assistant, I can help you create better resumes and provide career guidance. What would you like to know?",
            "I'm designed to help you build professional resumes and provide career insights. How can I assist you today?"
        ]
        
        import random
        return jsonify({
            "response": random.choice(fallback_responses),
            "status": "fallback"
        })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)