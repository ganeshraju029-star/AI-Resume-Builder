# AI Resume & Portfolio Builder with Firebase Backend

A complete full-stack application for generating and managing AI-powered resumes using Firebase as the database backend.

## Features

- **Resume Generation**: Create professional resumes from user input
- **Firebase Integration**: All resumes are stored in Firestore database
- **CRUD Operations**: Create, Read, Update, and Delete resumes
- **Input Validation**: Server-side validation and sanitization
- **Modern UI**: Clean, responsive interface with real-time updates
- **Error Handling**: Comprehensive error handling throughout the application

## Project Structure

```
ai-resume-backend/
├── app.py                 # Main Flask application with API endpoints
├── firebase_config.py     # Firebase configuration and initialization
├── validation.py          # Input validation and sanitization functions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (Firebase credentials)
├── AICTEPROJ.html        # Frontend HTML file
└── README.md             # This file
```

## Setup Instructions

### 1. Firebase Project Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Enable Firestore Database in your project
4. Create a service account:
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Download the JSON file

### 2. Environment Configuration

#### Option A: Using Service Account File (Recommended)
1. Place the downloaded service account JSON file in your project directory
2. Rename it to `serviceAccountKey.json`
3. Update your `.env` file:
   ```env
   FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
   ```

#### Option B: Using Environment Variables
1. Open the downloaded JSON file and copy the values
2. Update your `.env` file with your actual Firebase credentials:
   ```env
   FIREBASE_PROJECT_ID=your-actual-project-id
   FIREBASE_PRIVATE_KEY_ID=your-actual-private-key-id
   FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_ACTUAL_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
   FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-actual-project-id.iam.gserviceaccount.com
   FIREBASE_CLIENT_ID=your-actual-client-id
   FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
   FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
   FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-actual-project-id.iam.gserviceaccount.com
   ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The backend will start on `http://localhost:5000`

### 5. Open the Frontend

Open `AICTEPROJ.html` in your web browser or serve it with a web server.

## API Endpoints

### Resume Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate-resume` | Create a new resume |
| GET | `/resumes` | Get all resumes |
| GET | `/resumes/{id}` | Get a specific resume |
| PUT | `/resumes/{id}` | Update a resume |
| DELETE | `/resumes/{id}` | Delete a resume |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check if backend is running |

## Request/Response Examples

### Create Resume
```bash
POST /generate-resume
Content-Type: application/json

{
  "name": "John Doe",
  "education": "B.Tech in Computer Science",
  "skills": "Python, JavaScript, React, Node.js",
  "projects": "E-commerce website, Mobile app",
  "goal": "Become a full-stack developer"
}
```

Response:
```json
{
  "resume": "John Doe\n-------------------------\nEducation:\nB.Tech in Computer Science\n\nSkills:\nPython, JavaScript, React, Node.js\n\nProjects:\nE-commerce website, Mobile app\n\nCareer Goal:\nBecome a full-stack developer",
  "id": "uuid-here",
  "message": "Resume saved successfully!"
}
```

## Frontend Features

- **Form Validation**: Client-side validation for all required fields
- **Resume List**: View all saved resumes with creation dates
- **Load Resume**: Click any resume to load it for editing
- **Update/Delete**: Modify or remove existing resumes
- **Real-time Feedback**: Success/error messages for all operations
- **Responsive Design**: Works on desktop and mobile devices

## Security Features

- **Input Sanitization**: Removes potentially harmful characters
- **Validation**: Server-side validation for all inputs
- **Error Handling**: Proper HTTP status codes and error messages
- **CORS**: Cross-origin resource sharing configured for frontend

## Deployment Notes

### Environment Variables
Make sure to set proper environment variables in production:
- Never commit `.env` file to version control
- Use proper secrets management in production
- Ensure Firebase service account has appropriate permissions

### Firebase Security Rules
Configure Firestore security rules in Firebase Console:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /resumes/{resumeId} {
      allow read, write: if request.time < timestamp.date(2025, 1, 1);
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Firebase Connection Error**
   - Verify your Firebase credentials in `.env`
   - Check if Firestore is enabled in your Firebase project
   - Ensure service account has proper permissions

2. **Module Import Errors**
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility

3. **CORS Issues**
   - Backend should be running before accessing frontend
   - Check if Flask CORS is properly configured

4. **Environment Variables Not Loading**
   - Ensure `.env` file is in the same directory as `app.py`
   - Install `python-dotenv` package

## Development

### Adding New Features

1. **New API Endpoints**: Add routes in `app.py`
2. **Database Operations**: Use the `db` object from `firebase_config.py`
3. **Validation**: Add validation rules in `validation.py`
4. **Frontend**: Update `AICTEPROJ.html` with new JavaScript functions

### Testing

Test the API endpoints using:
- Postman
- curl commands
- Browser developer tools

## License

This project is for educational purposes as part of an AICTE student project.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify Firebase configuration
3. Ensure all dependencies are installed
4. Check console logs for detailed error messages
