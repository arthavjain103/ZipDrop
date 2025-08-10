from django.shortcuts import redirect, render
import os
import uuid
from sendEverywhere import settings
from .models import File
from django.http import FileResponse
from . import task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Feedback
from django.contrib import messages


def create_folder(folder_path):
    """Creates a folder if it doesn't exist."""
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def download(request_code):
    obj = File.objects.get(request_code=request_code)
    filename = obj.model_attribute_name.path
    response = FileResponse(open(filename, 'rb'))
    return response


def index(request):
    context = {
        "active_nav": "home",
        "user": request.user
    }

    # Handle File Upload
    if request.method == "POST" and request.FILES.get("file"):
        random_uuid = uuid.uuid4()
        file = request.FILES["file"]

        # Extract filename and extension
        split_tup = os.path.splitext(file.name)
        file_name = split_tup[0]
        file_extension = split_tup[1]

        filename = f"{random_uuid}{file_extension}"

        # Save file to media folder
        create_folder(os.path.join(settings.MEDIA_ROOT, "file/"))

        with open(os.path.join(settings.MEDIA_ROOT, "file/", filename), "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        path = os.path.join(settings.MEDIA_ROOT, "file/", filename)

        try:
            fileobject = File(uuid=random_uuid, file=file, name=file_name, path=path)
            fileobject.save()
        except:
            messages.error(request, "Could not upload file")
            return render(request, "index.html", context)

        # Show code or link with expiry time
        if "request_code" in request.POST:
            context.update({
                "request_code": fileobject.request_code,
                "expires_at": fileobject.expiration_time
            })
        elif "request_link" in request.POST:
            context.update({
                "Link": request.build_absolute_uri(fileobject.file.url),
                "expires_at": fileobject.expiration_time
            })

        return render(request, "index.html", context)

    # Handle File Download by Code
    elif request.method == "GET" and request.GET.get("request_code"):
        request_code = request.GET.get("request_code")
        try:
            obj = File.objects.get(request_code=request_code)
            
            if obj.is_expired():
                messages.error(request, "⚠️ This file/code has expired and is no longer available.")
                return render(request, "index.html", context)
            
            filename = obj.path
            response = FileResponse(
                open(filename, 'rb'), as_attachment=True, filename=obj.file.name
            )
            return response
        except File.DoesNotExist:
            messages.error(request, "❌ Request code doesn't exist")
            return render(request, "index.html", context)

    # Default: show upload page
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html", {'active_nav': 'about'})


def services(request):
    return render(request, "services.html", {'active_nav': 'services'})


def contact(request):
    return render(request, "contact.html", {'active_nav': 'contact'})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            return redirect("register")
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        firstName = request.POST.get("firstName")
        email = request.POST.get("email")

        user = User.objects.create_user(
            email=email, username=username, password=password, first_name=firstName
        )
        user.save()
        return redirect("index")
    return render(request, "register.html")


def feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            Feedback.objects.create(name=name, email=email, message=message)
            messages.success(request, "✅ Thank you for your feedback! We will get back to you.")
            return redirect("contact")

    return render(request, "contact.html")
