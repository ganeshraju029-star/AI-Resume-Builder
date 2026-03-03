def validate_resume_data(data):
    """Validate resume data before processing"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'education', 'skills', 'projects', 'goal']
    for field in required_fields:
        if not data.get(field, '').strip():
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Field length validations
    if data.get('name') and len(data['name'].strip()) > 100:
        errors.append("Name must be less than 100 characters")
    
    if data.get('education') and len(data['education'].strip()) > 500:
        errors.append("Education must be less than 500 characters")
    
    if data.get('skills') and len(data['skills'].strip()) > 1000:
        errors.append("Skills must be less than 1000 characters")
    
    if data.get('projects') and len(data['projects'].strip()) > 2000:
        errors.append("Projects must be less than 2000 characters")
    
    if data.get('goal') and len(data['goal'].strip()) > 200:
        errors.append("Career goal must be less than 200 characters")
    
    return errors

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    dangerous_chars = ['<', '>', '"', "'", '&', '`', '=', '$', '{', '}']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()
