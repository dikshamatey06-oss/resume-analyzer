from flask import Flask, render_template, request
import re
import PyPDF2
from docx import Document

app = Flask(__name__)

SKILLS_DB = [

    # AI / ML

    "ai",
    "artificial intelligence",
    "generative ai",
    "agentic ai",
    "machine learning",
    "deep learning",
    "nlp",
    "natural language processing",
    "computer vision",
    "llm",
    "large language models",
    "rag",
    "retrieval augmented generation",
    "prompt engineering",
    "fine tuning",
    "reinforcement learning",
    "hugging face",
    "langchain",
    "langgraph",
    "llamaindex",
    "openai",
    "gemini",
    "claude",
    "mistral",
    "vector database",
    "faiss",
    "pinecone",
    "chroma db",

    # Data Science / Analytics

    "data analysis",
    "data science",
    "data visualization",
    "business intelligence",
    "statistics",
    "predictive analytics",
    "data mining",
    "data cleaning",
    "data warehousing",
    "etl",
    "power bi",
    "tableau",
    "excel",
    "power query",
    "dax",
    "looker",

    # Programming Languages

    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "php",
    "ruby",
    "go",
    "golang",
    "rust",
    "swift",
    "kotlin",
    "dart",
    "r",
    "matlab",

    # Frontend

    "html",
    "css",
    "bootstrap",
    "tailwind css",
    "react",
    "next.js",
    "redux",
    "angular",
    "vue.js",
    "jquery",

    # Backend

    "node.js",
    "node",
    "express",
    "django",
    "flask",
    "fastapi",
    "spring boot",
    "laravel",
    "asp.net",
    "rest api",
    "graphql",
    "microservices",
    "jwt",

    # Databases

    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "oracle",
    "firebase",
    "redis",
    "supabase",

    # Python Libraries

    "pandas",
    "numpy",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "plotly",
    "opencv",
    "beautifulsoup",
    "selenium",
    "keras",

    # Deep Learning Frameworks

    "tensorflow",
    "pytorch",

    # Cloud / DevOps

    "aws",
    "azure",
    "gcp",
    "google cloud",
    "docker",
    "kubernetes",
    "terraform",
    "jenkins",
    "github actions",
    "ci/cd",
    "nginx",
    "linux",

    # Version Control

    "git",
    "github",
    "gitlab",
    "bitbucket",

    # Mobile Development

    "android",
    "flutter",
    "react native",
    "ios",
    "dart",
    "kotlin",
    "swift",

    # Cybersecurity

    "cybersecurity",
    "ethical hacking",
    "penetration testing",
    "network security",
    "cryptography",
    "owasp",

    # Testing

    "unit testing",
    "integration testing",
    "pytest",
    "jest",
    "selenium testing",

    # Software Engineering

    "oop",
    "object oriented programming",
    "design patterns",
    "system design",
    "agile",
    "scrum",

    # Tools

    "jira",
    "postman",
    "figma",
    "canva",
    "weka"

    "data structures",
"algorithms",
"communication",
"reporting",
"predictive analytics",
"data pipelines",
"spark",
"airflow",
"terraform",
"jenkins",
"ci/cd",
"github actions",
"nginx",
"monitoring",
"hibernate",
"xml",
"mobile development",
"firewalls",
"security testing",
"risk assessment",
"database",
"performance tuning",
"backup",
"recovery",
"testing",
"automation testing",
"quality assurance",
"bug tracking",
"wireframing",
"prototyping",
"user research",
"ux",
"ui",
"adobe xd",
"mockups"
]

JOB_ROLES = {


"Frontend Developer": [
    "html", "css", "javascript", "typescript",
    "react", "redux", "bootstrap", "tailwind css",
    "next.js", "figma"
],

"Backend Developer": [
    "python", "django", "flask", "fastapi",
    "sql", "mongodb", "postgresql",
    "rest api", "jwt", "microservices"
],

"Full Stack Developer": [
    "html", "css", "javascript", "react",
    "node.js", "express", "mongodb",
    "sql", "rest api", "git"
],

"Software Engineer": [
    "python", "java", "c++",
    "oop", "sql", "git",
    "github", "system design",
    "data structures", "algorithms"
],

"Data Analyst": [
    "python", "sql", "excel",
    "power bi", "tableau",
    "data analysis", "statistics",
    "data visualization",
    "business intelligence",
    "power query"
],

"Business Analyst": [
    "excel", "sql", "power bi",
    "tableau", "business intelligence",
    "data analysis", "statistics",
    "communication", "reporting",
    "data visualization"
],

"Data Scientist": [
    "python", "machine learning",
    "data science", "pandas",
    "numpy", "scikit-learn",
    "statistics",
    "data visualization",
    "deep learning",
    "predictive analytics"
],

"Data Engineer": [
    "python", "sql",
    "etl", "data warehousing",
    "postgresql", "aws",
    "data pipelines",
    "spark",
    "airflow",
    "mongodb"
],

"ML Engineer": [
    "python",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "numpy",
    "pandas",
    "computer vision",
    "nlp"
],

"AI Engineer": [
    "python",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "hugging face",
    "data science",
    "scikit-learn"
],

"Generative AI Engineer": [
    "python",
    "generative ai",
    "llm",
    "rag",
    "langchain",
    "langgraph",
    "openai",
    "prompt engineering",
    "vector database",
    "hugging face"
],

"NLP Engineer": [
    "python",
    "nlp",
    "machine learning",
    "deep learning",
    "hugging face",
    "tensorflow",
    "pytorch",
    "llm",
    "generative ai",
    "langchain"
],

"Cloud Engineer": [
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "linux",
    "terraform",
    "git",
    "jenkins",
    "ci/cd"
],

"AWS Cloud Engineer": [
    "aws",
    "docker",
    "kubernetes",
    "linux",
    "terraform",
    "jenkins",
    "git",
    "github actions",
    "ci/cd",
    "nginx"
],

"DevOps Engineer": [
    "docker",
    "kubernetes",
    "aws",
    "linux",
    "git",
    "github",
    "jenkins",
    "terraform",
    "ci/cd",
    "nginx"
],

"Site Reliability Engineer": [
    "linux",
    "aws",
    "docker",
    "kubernetes",
    "terraform",
    "jenkins",
    "monitoring",
    "ci/cd",
    "nginx",
    "git"
],

"React Developer": [
    "html",
    "css",
    "javascript",
    "typescript",
    "react",
    "redux",
    "next.js",
    "bootstrap",
    "tailwind css",
    "figma"
],

"Python Developer": [
    "python",
    "django",
    "flask",
    "fastapi",
    "sql",
    "postgresql",
    "rest api",
    "jwt",
    "git",
    "mongodb"
],

"Java Developer": [
    "java",
    "spring boot",
    "sql",
    "rest api",
    "microservices",
    "git",
    "github",
    "mongodb",
    "oop",
    "hibernate"
],

"Android Developer": [
    "java",
    "kotlin",
    "android",
    "firebase",
    "git",
    "sql",
    "rest api",
    "xml",
    "mobile development",
    "github"
],

"Flutter Developer": [
    "flutter",
    "dart",
    "firebase",
    "rest api",
    "git",
    "mobile development",
    "android",
    "ios",
    "github",
    "sql"
],

"Cybersecurity Analyst": [
    "cybersecurity",
    "network security",
    "ethical hacking",
    "penetration testing",
    "linux",
    "cryptography",
    "owasp",
    "firewalls",
    "security testing",
    "risk assessment"
],

"Database Administrator": [
    "sql",
    "mysql",
    "postgresql",
    "oracle",
    "database",
    "performance tuning",
    "backup",
    "recovery",
    "data warehousing",
    "linux"
],

"QA Engineer": [
    "testing",
    "unit testing",
    "integration testing",
    "pytest",
    "selenium",
    "automation testing",
    "jira",
    "git",
    "quality assurance",
    "bug tracking"
],

"UI UX Designer": [
    "figma",
    "canva",
    "wireframing",
    "prototyping",
    "design",
    "user research",
    "ux",
    "ui",
    "adobe xd",
    "mockups"
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

    found_skills = []

    for skill in SKILLS_DB:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills

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
        if not text.strip():

         return render_template(
        "landing.html",
        error="No text could be extracted from the uploaded resume. Please upload a valid PDF, DOCX, or TXT resume."
    )

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
