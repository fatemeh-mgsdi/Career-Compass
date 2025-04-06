# Career Compass 🚀

Career Compass is an AI-powered career development platform that helps job seekers enhance their professional journey through intelligent resume analysis, job matching, and interview practice.

## 🌟 Features

### 📝 Resume Analysis
- Upload and analyze resumes using AI
- Get detailed feedback on resume content and structure
- Receive ATS (Applicant Tracking System) compatibility scores
- Get suggestions for improvement
- Track analysis history and progress

### 💼 Job Matching
- Smart job recommendations based on resume content
- Detailed job listings with company information
- Easy application tracking
- Job search with advanced filters
- Save favorite jobs

### 🎯 Interview Practice
- AI-generated interview questions based on your resume and job descriptions
- Practice technical, behavioral, and system design interviews
- Get instant feedback on your answers
- Track your interview performance
- Receive improvement suggestions

## 🛠️ Technology Stack

- **Backend**: Django 5.0
- **Database**: PostgreSQL
- **AI Integration**: OpenAI GPT-4
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Postman Collection
- **File Storage**: Local/Cloud storage for resumes

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/fatemeh-mgsdi/Career-Compass.git
cd Career-Compass
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## 📚 API Documentation

### Authentication

All API endpoints require authentication using JWT tokens.

1. **Login**
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```

2. **Refresh Token**
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

### Resume Management

1. **Upload Resume**
```http
POST /api/resumes/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data

file: your_resume.pdf
title: "My Resume"
```

2. **Analyze Resume**
```http
POST /api/resumes/{id}/analyze/
Authorization: Bearer your_access_token
```

3. **Get Analysis**
```http
GET /api/resumes/{id}/analysis/
Authorization: Bearer your_access_token
```

### Interview Practice

1. **Create Interview**
```http
POST /api/interviews/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "resume": 1,
    "title": "Python Developer Interview",
    "interview_type": "technical",
    "job_description": "Looking for a Python developer..."
}
```

2. **Generate Questions**
```http
POST /api/interviews/{id}/generate_questions/
Authorization: Bearer your_access_token
```

3. **Submit Answer**
```http
POST /api/interviews/{id}/submit_answer/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "question_id": 1,
    "answer": "Your detailed answer..."
}
```

For a complete API documentation, check out our [Postman Collection](Career_Compass_API.postman_collection.json).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Fatemeh Mgsdi** - *Initial work* - [fatemeh-mgsdi](https://github.com/fatemeh-mgsdi)

## 🙏 Acknowledgments

- OpenAI for providing the AI capabilities
- Django community for the amazing framework
- All contributors and users of Career Compass 