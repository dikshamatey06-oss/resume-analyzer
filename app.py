from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

SKILLS_DB = [
    "python", "java", "html", "css", "javascript", "sql",
    "machine learning", "data analysis", "react", "node",
    "flask", "excel", "power bi", "django"
]

JOB_ROLES = {
    "Data Analyst": ["python", "sql", "excel", "power bi", "data analysis"],
    "Web Developer": ["html", "css", "javascript", "react", "node"],
    "ML Engineer": ["python", "machine learning", "data analysis"],
    "Backend Developer": ["python", "django", "flask", "sql"]
}

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

def extract_skills(text):
    return [skill for skill in SKILLS_DB if skill in text]

def predict_role(skills):
    scores = {role: len(set(skills) & set(req)) for role, req in JOB_ROLES.items()}
    return max(scores, key=scores.get) if skills else "No Role Detected"

def missing_skills(role, skills):
    return [s for s in JOB_ROLES.get(role, []) if s not in skills]

def resume_score(skills):
    return min(len(skills) * 10, 100)

def generate_feedback(role, missing, score):
    if score < 40:
        return f"Your resume is not strongly aligned with the {role} role. Focus on adding key skills like {', '.join(missing[:3])} and include more relevant projects."
    elif score < 70:
        return f"You have a good base for the {role} role. Improve by adding skills such as {', '.join(missing[:3])} and strengthening project descriptions."
    else:
        return f"Your resume is well aligned with the {role} role. To stand out further, add advanced projects, certifications, or real-world experience."

@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    role = ""
    missing = []
    score = 0
    feedback = ""

    if request.method == "POST":
        file = request.files["resume"]

        text = extract_text_from_pdf(file)
        skills = extract_skills(text)
        role = predict_role(skills)
        missing = missing_skills(role, skills)
        score = resume_score(skills)
        feedback = generate_feedback(role, missing, score)

    return render_template("index.html", skills=skills, role=role, missing=missing, score=score, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)