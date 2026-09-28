import pdfplumber
import re

SKILLS = [
    "Python", "Java", "C", "C++", "JavaScript",
    "HTML", "CSS", "Django", "Flask", "React",
    "Node.js", "SQL", "MySQL", "MongoDB",
    "Machine Learning", "Deep Learning",
    "Pandas", "NumPy", "Git", "AWS"
]

def extract_resume_data(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.findall(r'\+?\d[\d\s-]{8,15}', text)

    skills_found = []

    for skill in SKILLS:
        if skill.lower() in text.lower():
            skills_found.append(skill)

    return {
        "text": text,
        "email": email,
        "phone": phone,
        "skills": skills_found
    }