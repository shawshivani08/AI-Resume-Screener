from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Resume
from .parser import extract_resume_data


# ---------------- HOME ----------------

def home(request):
    return render(request, "index.html")


# ---------------- LOGIN ----------------

def login_view(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid Email or Password")

    return render(request, "login.html")


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )

        messages.success(request, "Registration Successful")
        return redirect("login")

    return render(request, "register.html")


# ---------------- DASHBOARD ----------------

def dashboard(request):
    return render(request, "dashboard.html")


# ---------------- LOGOUT ----------------

def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- JOB DESCRIPTION ----------------

def job_description(request):

    if request.method == "POST":

        jd = request.POST.get("job_description")

        request.session["jd"] = jd

        return redirect("upload")

    return render(request, "job_description.html")


# ---------------- RESUME UPLOAD ----------------

def upload_resume(request):

    if request.method == "POST":

        name = request.POST.get("candidate_name")
        email = request.POST.get("email")
        jd = request.POST.get("job_description", "")
        file = request.FILES.get("resume")

        # Save Resume
        resume = Resume.objects.create(
            candidate_name=name,
            email=email,
            resume=file
        )

        # Parse Resume
        resume_data = extract_resume_data(resume.resume.path)

        resume_text = resume_data["text"]

        print("=" * 50)
        print("RESUME TEXT:")
        print(resume_text)

        print("=" * 50)
        print("JOB DESCRIPTION:")
        print(jd)

        skills = [
            "Python",
            "Django",
            "HTML",
            "CSS",
            "JavaScript",
            "SQL",
            "MySQL",
            "Git"
        ]

        matched = 0
        matched_skills = []

        for skill in skills:

            if skill.lower() in jd.lower() and skill.lower() in resume_text.lower():
                matched += 1
                matched_skills.append(skill)

        score = int((matched / len(skills)) * 100)

        print("Matched Skills:", matched_skills)
        print("Score:", score)

        resume.score = score
        resume.save()

        resume_data["score"] = score
        resume_data["matched_skills"] = matched_skills

        return render(request, "result.html", {
            "data": resume_data
        })

    return render(request, "upload_resume.html")


        # Job Description Session se lo
    jd = request.POST.get("job_description", "")

        # Resume Text
    resume_text = resume_data["text"]

    matched = 0

    skills = [
            "Python",
            "Django",
            "HTML",
            "CSS",
            "JavaScript",
            "SQL",
            "MySQL",
            "Git"
        ]

    matched_skills = []

        # Matching
    for skill in skills:
            if skill.lower() in jd.lower() and skill.lower() in resume_text.lower():
                matched += 1
                matched_skills.append(skill)

        # Score Calculate
    score = int((matched / len(skills)) * 100)

        # Score Database me Save
    resume.score = score
    resume.save()

        # Result Page ke liye Data
    resume_data["score"] = score
    resume_data["matched_skills"] = matched_skills

    return render(request, "result.html", {
            "data": resume_data
        })

    return render(request, "upload_resume.html")
def ranking(request):

    resumes = Resume.objects.all().order_by("-score")

    return render(request, "ranking.html", {
        "resumes": resumes
    })
from .models import Resume

def dashboard(request):

    resumes = Resume.objects.all()

    total = resumes.count()

    selected = resumes.filter(score__gte=80).count()

    shortlisted = resumes.filter(score__gte=60, score__lt=80).count()

    rejected = resumes.filter(score__lt=60).count()

    return render(request, "dashboard.html", {
        "total": total,
        "selected": selected,
        "shortlisted": shortlisted,
        "rejected": rejected
    })