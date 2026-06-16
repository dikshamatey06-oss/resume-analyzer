# ResumeAI

ResumeAI is an AI-powered resume analysis platform that helps users evaluate their resumes against ATS (Applicant Tracking Systems) and job descriptions.

The application analyzes resumes, identifies strengths and skill gaps, predicts suitable job roles, and provides actionable recommendations to improve job match scores.

---

## Features

### ATS Compatibility Analysis
- ATS score calculation
- Resume structure evaluation
- Resume health checks
- Section detection (Skills, Education, Projects, Experience)

### Skill Analysis
- Extracts skills from resumes
- Highlights missing skills
- Identifies top strengths
- Provides skill gap insights

### Role Prediction
- Matches resumes against multiple job roles
- Role-wise compatibility scores
- Best-fit role recommendation

### Job Description Matching
- Compare resumes against custom job descriptions
- Keyword coverage analysis
- Missing keyword detection
- Match percentage calculation

### Analytics Dashboard
- ATS score visualization
- Role match analytics
- Resume insights
- Score breakdown
- Improvement recommendations

---

## Tech Stack

### Backend
- Python
- Flask

### Frontend
- HTML
- CSS
- Bootstrap 5
- Jinja2

### Resume Processing
- PyPDF2
- Regular Expressions (Regex)

---

## Project Structure

```text
ResumeAI/
│
├── app.py
├── resume_analyzer.py
│
├── templates/
│   ├── landing.html
│   └── dashboard.html
│
├── static/
│   └── style.css
│
├── uploads/
│
└── README.md
```

---

## How It Works

1. Upload a PDF resume.
2. ResumeAI extracts resume content.
3. Skills are identified using a predefined skills database.
4. ATS score is calculated.
5. Suitable job roles are predicted.
6. Missing skills and strengths are identified.
7. If a Job Description is provided:
   - Keywords are extracted
   - Match percentage is calculated
   - Missing requirements are highlighted
8. Results are displayed on an interactive dashboard.

---

## Sample Insights

- ATS Compatibility Score
- Resume Health Check
- Top Strengths
- Missing Skills
- Job Match Score
- Keyword Coverage
- Recommended Next Steps

---

## Future Improvements

- OpenAI-powered resume feedback
- Resume rewriting suggestions
- Resume PDF export
- User authentication
- Resume history tracking
- Real-time job recommendation engine

---

## Author

Developed by Diksha Matey

Aspiring AI & Data Science Engineer passionate about building practical AI-powered applications.
