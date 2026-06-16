from flask import Flask, render_template, request
import PyPDF2
from docx import Document

app = Flask(__name__)

SKILLS_DB = [

    "python",
    "java",
    "c",
    "c++",

    "html",
    "css",
    "javascript",
    "typescript",

    "react",
    "node",
    "express",

    "django",
    "flask",
    "spring boot",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "machine learning",
    "deep learning",
    "data analysis",
    "data science",

    "pandas",
    "numpy",
    "scikit-learn",

    "tensorflow",
    "pytorch",

    "power bi",
    "tableau",
    "excel",

    "aws",
    "azure",
    "docker",
    "kubernetes",

    "linux",
    "git",
    "github",

    "rest api"
]

JOB_ROLES = {

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "typescript"
    ],

    "Backend Developer": [
        "python",
        "django",
        "flask",
        "sql",
        "mongodb",
        "rest api"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node",
        "express",
        "mongodb"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data analysis"
    ],

    "Data Scientist": [
        "python",
        "machine learning",
        "data science",
        "pandas",
        "numpy",
        "scikit-learn"
    ],

    "ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn"
    ],

    "Cloud Engineer": [
        "aws",
        "azure",
        "docker",
        "kubernetes",
        "linux",
        "git"
    ],

    "DevOps Engineer": [
        "docker",
        "kubernetes",
        "aws",
        "git",
        "github",
        "linux"
    ]
}


def extract_text(file):

    filename = file.filename.lower()

    # PDF

    if filename.endswith(".pdf"):

        reader = PyPDF2.PdfReader(file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

        return text.lower()

    # DOCX

    elif filename.endswith(".docx"):

        doc = Document(file)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

        return text.lower()

    # TXT

    elif filename.endswith(".txt"):

        text = file.read().decode(
            "utf-8",
            errors="ignore"
        )

        return text.lower()

    return ""

def extract_skills(text):
    return [skill for skill in SKILLS_DB if skill in text]

def detect_sections(text):

    sections = {
        "Skills": False,
        "Education": False,
        "Projects": False,
        "Experience": False
    }

    text = text.lower()

    if "skills" in text:
        sections["Skills"] = True

    if "education" in text:
        sections["Education"] = True

    if "project" in text or "projects" in text:
        sections["Projects"] = True

    if "experience" in text or "work experience" in text:
        sections["Experience"] = True

    return sections


def role_match_scores(skills):

    scores = {}

    for role, required_skills in JOB_ROLES.items():

        matched = len(
            set(skills) & set(required_skills)
        )

        percentage = int(
            (matched / len(required_skills)) * 100
        )

        scores[role] = percentage

    return scores


def predict_role(skills):

    scores = {
        role: len(set(skills) & set(req))
        for role, req in JOB_ROLES.items()
    }

    return max(scores, key=scores.get) if skills else "No Role Detected"


def missing_skills(role, skills):
    return [
        skill
        for skill in JOB_ROLES.get(role, [])
        if skill not in skills
    ]

def top_strengths(role, skills):

    required = JOB_ROLES.get(role, [])

    return [
        skill
        for skill in skills
        if skill in required
    ][:5]

def generate_recommendations(missing):

    recommendations = []

    recommendation_map = {

        "sql": "Learn SQL fundamentals and database querying.",

        "python": "Strengthen Python programming skills through projects.",

        "machine learning": "Build ML projects using Scikit-Learn.",

        "data analysis": "Practice data cleaning and visualization.",

        "react": "Create frontend projects using React.",

        "docker": "Learn containerization using Docker.",

        "aws": "Gain experience with AWS cloud services.",

        "power bi": "Build interactive dashboards using Power BI.",

        "tableau": "Practice data visualization with Tableau."
    }

    for skill in missing:

        if skill in recommendation_map:
            recommendations.append(
                recommendation_map[skill]
            )

    return recommendations

def generate_checklist(role, missing):

    checklist = []

    for skill in missing:

        checklist.append(
            f"Add projects demonstrating {skill}"
        )

        checklist.append(
            f"Add certifications related to {skill}"
        )

    checklist.append(
        "Quantify achievements with numbers and impact"
    )

    checklist.append(
        "Add GitHub or portfolio links"
    )

    return checklist[:6]

def resume_score(role, skills):

    required = JOB_ROLES.get(role, [])

    if not required:
        return 0

    matched = len(
        set(skills) & set(required)
    )

    score = int(
        (matched / len(required)) * 100
    )

    return score

def keyword_coverage(role, skills):

    required = JOB_ROLES.get(role, [])

    matched = len(
        set(skills) & set(required)
    )

    return {
        "required": len(required),
        "matched": matched,
        "percentage": int(
            (matched / len(required)) * 100
        ) if required else 0
    }

def jd_match(skills, job_description):

    jd_skills = [
        skill
        for skill in SKILLS_DB
        if skill in job_description
    ]

    matched_skills = [
        skill
        for skill in jd_skills
        if skill in skills
    ]

    missing_skills_list = [
        skill
        for skill in jd_skills
        if skill not in skills
    ]

    score = int(
        (len(matched_skills) / len(jd_skills)) * 100
    ) if jd_skills else 0

    return {
        "score": score,
        "matched": matched_skills,
        "missing": missing_skills_list
    }

def jd_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Add a project demonstrating {skill}"
        )

        recommendations.append(
            f"Highlight experience related to {skill}"
        )

    return recommendations[:5]

def score_breakdown(role, skills, sections):

    required = JOB_ROLES.get(role, [])

    # Skills Score (50)

    skill_score = int(
        (len(set(skills) & set(required))
        / len(required)) * 50
    ) if required else 0

    # Structure Score (25)

    structure_score = (
        sum(sections.values()) / 4
    ) * 25

    # Role Alignment (25)

    role_score = int(
        (len(set(skills) & set(required))
        / len(required)) * 25
    ) if required else 0

    final_score = (
        skill_score +
        structure_score +
        role_score
    )

    return {
        "skills_score": int(skill_score),
        "structure_score": int(structure_score),
        "role_score": int(role_score),
        "final_score": int(final_score)
    }


def generate_feedback(role, missing, score):

    if score < 40:
        return (
            f"Your resume is not strongly aligned with the {role} role. "
            f"Focus on adding key skills like {', '.join(missing[:3])} "
            f"and include more relevant projects."
        )

    elif score < 70:
        return (
            f"You have a good base for the {role} role. "
            f"Improve by adding skills such as {', '.join(missing[:3])} "
            f"and strengthening project descriptions."
        )

    else:
        return (
            f"Your resume is well aligned with the {role} role. "
            f"To stand out further, add advanced projects, certifications, "
            f"or real-world experience."
        )


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["resume"]
        job_description = request.form.get(
    "job_description",
    ""
).lower()

        text = extract_text(file)

        skills = extract_skills(text)
        jd_results = jd_match(
    skills,
    job_description
)

        role = predict_role(skills)

        role_scores = role_match_scores(skills)

        missing = missing_skills(role, skills)

        strengths = top_strengths(role, skills)


        recommendations = generate_recommendations(
            missing
        )
        checklist = generate_checklist(
    role,
    missing
)

        score = resume_score(role, skills)

        coverage = keyword_coverage(
    role,
    skills
)

        feedback = generate_feedback(
            role,
            missing,
            score
        )

        sections = detect_sections(text)

        jd_tips = jd_recommendations(
    jd_results["missing"]
)

        breakdown = score_breakdown(
          role,
          skills,
          sections
)
        return render_template(
    "dashboard.html",
    skills=skills,
    role=role,
    missing=missing,
    score=score,
    feedback=feedback,
    role_scores=role_scores,
    recommendations=recommendations,
    sections=sections,
    breakdown=breakdown,
    strengths=strengths,
    coverage=coverage,
    checklist=checklist,
    jd_results=jd_results,
    jd_tips=jd_tips,
)
    return render_template("landing.html")


if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True)
