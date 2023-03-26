from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm, ApplicantForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from .models import Destination, Destination_desc, Applicant


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


class Reservation:
    pass


def search(request):
    try:
        loc_list = Destination.objects.all()
        if request.method == 'POST':
            place_user = request.POST['place']
            try:
                get_object_or_404(Destination_desc, province=place_user)
                # loc_desc_list = Destination_desc.objects.get()
            except MultipleObjectsReturned:
                loc_desc_list = Destination_desc.objects.filter(province=place_user)
                available_list = Reservation.objects.filter(destination__province=place_user)
                return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                               'available_list': available_list,
                                                               'search_item': 'province'})
        else:
            price_selected = request.GET.get("price")
            available_list = Reservation.objects.all()
            print(price_selected)
            if price_selected == "2":
                loc_desc_list = Destination_desc.objects.filter(price__range=(0, 1000))
            elif price_selected == "3":
                loc_desc_list = Destination_desc.objects.filter(price__range=(1001, 2000))
            elif price_selected == "4":
                loc_desc_list = Destination_desc.objects.filter(price__gt=2000)
            return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                           'available_list': available_list, 'search_item': 'price'})

    except Exception as err:
        print(err)
        messages.info(request, 'Location not available')
        return redirect('skydive:index')


def search_loc(request, destination):
    loc_desc_list = Destination_desc.objects.filter(province=destination)
    loc_list = Destination.objects.all()
    available_list = Reservation.objects.all()
    return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                   'available_list': available_list, 'search_item': 'province'})


def type_skydive(request, skydive_type, desc_id):
    try:
        loc_desc_list = Destination_desc.objects.filter(type_skydive=skydive_type)
        loc_list = Destination.objects.all()
        available_list = Reservation.objects.all()
        print(skydive_type)
        return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                       'available_list': available_list, 'search_item': 'type_skydive'})
    except Exception as err:
        print(err)
        return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                       'search_item': 'type_skydive'})


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


def logout(request):
    auth.logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect('..')


@login_required(login_url='/skydive/login')
def booking(request, dest_id):
    passengerformset = formset_factory(PassengerForm, extra=1)
    if request.method == 'POST':
        formset = passengerformset(request.POST)
        if formset.is_valid():
            # selected_item_id = int(request.GET.get('desc_id'))
            date_selected = datetime.strptime(request.POST['booking_date'], "%Y-%m-%d").date()
            loc_desc = Destination_desc.objects.get(dest_id=dest_id)
            user = request.user
            total_fare = formset.total_form_count() * loc_desc.price
            # request.session['n'] = formset.total_form_count()
            booking_item = Booking.objects.create(user=user, booking_date=date_selected, total_fare=total_fare,
                                                  type_skydive=loc_desc.type_skydive, destination_desc=loc_desc)
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]
                passenger_detail = Passenger(first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'],
                                             age=form.cleaned_data['age'])
                passenger_detail.save()

                booking_item.passengers.add(passenger_detail)
                # booking_item = Booking(user=user, passengers=passenger_detail,
                #                       booking_date=date_selected, total_fare=total_fare,
                #                       type_skydive=loc_desc.type_skydive, destination_desc=loc_desc
                #                       )
            booking_item.save()

            HST = total_fare * 0.18
            HST = float("{:.2f}".format(HST))
            final_total = HST + total_fare
            return render(request, 'skydive/payment.html', {'person_count': formset.total_form_count(),
                                                            'total_fare': total_fare, 'HST': HST,
                                                            'final_total': final_total, 'province': loc_desc.province,
                                                            'bookingid': booking_item.booking_id})
    else:
        formset = passengerformset()
        return render(request, 'skydive/booking.html', {'formset': formset, 'dest_id': dest_id})


def about(request):
    return render(request, 'skydive/about.html')


class JoinUs(View):

    def get(self, request):
        form= ApplicantForm()
        return render(request, 'skydive/join_us.html', {'form': form})

    def post(self, request):
        form=ApplicantForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            if(Applicant.objects.filter(email=form.cleaned_data['email']).exists()):
                messages.error(request, 'You have already applied')
                return redirect('skydive:joinus')
            applicant= Applicant.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                resume=form.cleaned_data['resume'],
                cover_letter=form.cleaned_data['cover_letter'],
                comments=form.cleaned_data['comments']
            )
            applicant.save()
            messages.success(request, 'Application Successful Submitted')
            return redirect('skydive:joinus')
        else:
            print(form.errors)
            messages.error(request, 'Invalid data')
            return redirect('skydive:joinus')


class Register(View):

    def get(self, request):
        form = NewUserForm()
        return render(request, 'skydive/register.html', context={"register_form": form})

    def post(self, request):
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