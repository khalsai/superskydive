from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


# Create your views here.

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'skydive/reset.html'
    email_template_name = 'skydive/password_reset_email.html'
    subject_template_name = 'skydive/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('skydive:login')


# def reset(request):
#    return render(request, "skydive/reset.html")


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials...')
            return redirect('/skydive/login')
    else:
        return render(request, 'skydive/login.html')


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Username already exists.")
                return redirect('register')
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, "Email already exists.")
                return redirect('register')
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                messages.error(request, "Passwords do not match.")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user = user.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('login')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return redirect('register')

    else:
        form = NewUserForm()
        return render(request, 'skydive/register.html', context={"register_form": form})


def logout(request):
    auth.logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect('..')
