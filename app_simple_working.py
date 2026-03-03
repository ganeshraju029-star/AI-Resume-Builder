from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import random
import json

app = Flask(__name__)
CORS(app)

# Mock database for demo
resumes_db = {}

# Load knowledge base
try:
    with open('chatbot_knowledge.json', 'r') as f:
        knowledge_data = json.load(f)
except FileNotFoundError:
    knowledge_data = {}

@app.route("/")
def home():
    return "AI Resume Backend is running"

@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.json
    
    name = data.get("name", "")
    education = data.get("education", "")
    skills = data.get("skills", "")
    projects = data.get("projects", "")
    goal = data.get("goal", "")

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

    # Save to mock database
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
    
    resumes_db[resume_id] = resume_data
    
    return jsonify({
        "resume": resume_text.strip(),
        "id": resume_id,
        "message": "Resume saved successfully!"
    })

@app.route("/resumes", methods=["GET"])
def get_all_resumes():
    return jsonify({"resumes": list(resumes_db.values())})

@app.route("/resumes/<resume_id>", methods=["GET"])
def get_resume(resume_id):
    if resume_id in resumes_db:
        return jsonify(resumes_db[resume_id])
    else:
        return jsonify({"error": "Resume not found"}), 404

@app.route("/resumes/<resume_id>", methods=["PUT"])
def update_resume(resume_id):
    if resume_id not in resumes_db:
        return jsonify({"error": "Resume not found"}), 404
    
    data = request.json
    
    resume_data = {
        "id": resume_id,
        "name": data.get("name", ""),
        "education": data.get("education", ""),
        "skills": data.get("skills", ""),
        "projects": data.get("projects", ""),
        "goal": data.get("goal", ""),
        "updated_at": datetime.now().isoformat()
    }
    
    # Regenerate resume text
    resume_text = f"""
    {resume_data['name']}
    -------------------------
    Education:
    {resume_data['education']}

    Skills:
    {resume_data['skills']}

    Projects:
    {resume_data['projects']}

    Career Goal:
    {resume_data['goal']}
    """
    
    resume_data["resume_text"] = resume_text.strip()
    resume_data["created_at"] = resumes_db[resume_id]["created_at"]
    
    resumes_db[resume_id] = resume_data
    
    return jsonify({
        "message": "Resume updated successfully!",
        "resume": resume_text.strip()
    })

@app.route("/resumes/<resume_id>", methods=["DELETE"])
def delete_resume(resume_id):
    if resume_id not in resumes_db:
        return jsonify({"error": "Resume not found"}), 404
    
    del resumes_db[resume_id]
    return jsonify({"message": "Resume deleted successfully!"})

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").lower()
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    # Function to get random response from knowledge base
    def get_random_response(category, subcategory=None):
        if category in knowledge_data:
            if subcategory and subcategory in knowledge_data[category]:
                return random.choice(knowledge_data[category][subcategory])
            elif isinstance(knowledge_data[category], dict):
                # If category has subcategories, pick one randomly
                subcat = random.choice(list(knowledge_data[category].keys()))
                return random.choice(knowledge_data[category][subcat])
            elif isinstance(knowledge_data[category], list):
                return random.choice(knowledge_data[category])
        return None
    
    # Determine response based on keywords
    response = None
    
    # Resume related queries
    if any(keyword in user_message for keyword in ["resume", "cv", "format", "bullet"]):
        if any(keyword in user_message for keyword in ["format", "layout", "design"]):
            response = get_random_response("resume_tips", "format")
        else:
            response = get_random_response("resume_tips", "content")
        if not response:
            response = get_random_response("resume_tips")
    
    # Interview related queries
    elif any(keyword in user_message for keyword in ["interview", "question", "prepare"]):
        if any(keyword in user_message for keyword in ["before", "prepare"]):
            response = get_random_response("interview_preparation", "before")
        elif any(keyword in user_message for keyword in ["during", "while"]):
            response = get_random_response("interview_preparation", "during")
        elif any(keyword in user_message for keyword in ["after", "follow", "thank"]):
            response = get_random_response("interview_preparation", "after")
        else:
            response = get_random_response("interview_preparation")
    
    # Skills development
    elif any(keyword in user_message for keyword in ["skill", "learn", "develop", "training"]):
        if any(keyword in user_message for keyword in ["technical", "hard", "programming"]):
            response = get_random_response("skill_development", "technical")
        elif any(keyword in user_message for keyword in ["soft", "communication", "leadership"]):
            response = get_random_response("skill_development", "soft")
        else:
            response = get_random_response("skill_development")
    
    # Career advice
    elif any(keyword in user_message for keyword in ["career", "future", "goal", "path"]):
        if any(keyword in user_message for keyword in ["entry", "beginner", "start", "graduate"]):
            response = get_random_response("career_advice", "entry_level")
        elif any(keyword in user_message for keyword in ["mid", "experienced", "senior", "advance"]):
            response = get_random_response("career_advice", "mid_career")
        elif any(keyword in user_message for keyword in ["change", "switch", "transition"]):
            response = get_random_response("career_advice", "career_change")
        else:
            response = get_random_response("career_advice")
    
    # Job search
    elif any(keyword in user_message for keyword in ["job", "search", "apply", "application"]):
        if any(keyword in user_message for keyword in ["strategy", "plan", "approach"]):
            response = get_random_response("job_search", "strategy")
        elif any(keyword in user_message for keyword in ["network", "connect"]):
            response = get_random_response("job_search", "networking")
        else:
            response = get_random_response("job_search")
    
    # Portfolio development
    elif any(keyword in user_message for keyword in ["portfolio", "project", "showcase"]):
        if any(keyword in user_message for keyword in ["content", "work", "piece"]):
            response = get_random_response("portfolio_development", "content")
        elif any(keyword in user_message for keyword in ["presentation", "design", "layout"]):
            response = get_random_response("portfolio_development", "presentation")
        else:
            response = get_random_response("portfolio_development")
    
    # Professional branding
    elif any(keyword in user_message for keyword in ["brand", "linkedin", "website", "profile"]):
        if any(keyword in user_message for keyword in ["linkedin", "social"]):
            response = get_random_response("professional_branding", "linkedin")
        elif any(keyword in user_message for keyword in ["website", "personal", "blog"]):
            response = get_random_response("professional_branding", "personal_website")
        else:
            response = get_random_response("professional_branding")
    
    # Fallback to enhanced responses if no specific match
    if not response:
        enhanced_responses = [
            "I can help you with resume writing, interview preparation, skill development, career planning, job search strategies, portfolio building, and professional branding. What specific area would you like guidance on?",
            "Your professional development journey is unique! I can provide personalized advice on resumes, interviews, skills, career transitions, or job searching. What's your main focus right now?",
            "Building a successful career requires multiple skills. I can assist with resume optimization, interview techniques, skill development, career planning, or personal branding. What would you like to explore?",
            "I'm your AI career assistant! I can help with resume writing, interview preparation, skill development, career advice, job searching, portfolio creation, and professional branding. How can I support your career goals?",
            "Let's work together on your professional development! I can provide guidance on resumes, interviews, skills, career planning, job applications, portfolios, or personal branding. What's most important to you right now?"
        ]
        response = random.choice(enhanced_responses)
    
    return jsonify({
        "response": response,
        "status": "success"
    })

if __name__ == "__main__":
    print("Starting AI Resume Backend...")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    print("Or open the HTML file: AICTEPROJ.html")
    app.run(debug=True, host="0.0.0.0", port=5000)
